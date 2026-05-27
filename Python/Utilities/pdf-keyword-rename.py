

import os
from pypdf import PdfReader
from datetime import datetime
import re

folder = r"\\nu\GIS\Scripts\pdf-rename-test\test-ocr-output"

# Known vendors to detect
vendors = ["Amazon", "Home Depot", "Staples", "Grainger"]

# Keyword categories for items
keywords_map = {
    "pipe": ["pipe", "tubing"],
    "new": ["replace", "replacement"],
    "lumber": ["2x4", "plywood", "board"],
    "network": ["ethernet", "switch", "router"],
    "office": ["paper", "pens", "notebook"]
}

# Clean filename (Windows safe)
def clean_filename(s):
    return "".join(c for c in s if c.isalnum() or c in ("-", "_"))

# Extract date using multiple labels
def extract_date(text):
    date_labels = [
        "Order Placed:",
        "Order Date:",
        "Invoice Date:",
        "Purchase Date:",
        "Date:"
    ]

    for label in date_labels:
        # Format: January 20, 2026
        pattern1 = rf'{label}\s*([A-Za-z]+ \d{{1,2}}, \d{{4}})'
        match1 = re.search(pattern1, text, re.IGNORECASE)

        if match1:
            try:
                dt = datetime.strptime(match1.group(1), "%B %d, %Y")
                return dt.strftime("%Y-%m-%d")
            except:
                pass

        # Format: 01/20/2026
        pattern2 = rf'{label}\s*(\d{{2}}/\d{{2}}/\d{{4}})'
        match2 = re.search(pattern2, text, re.IGNORECASE)

        if match2:
            try:
                dt = datetime.strptime(match2.group(1), "%m/%d/%Y")
                return dt.strftime("%Y-%m-%d")
            except:
                pass

    return "nodate"

# Freeze file list to avoid iteration issues
files = list(os.listdir(folder))

for file in files:
    if not file.lower().endswith(".pdf"):
        continue

    print(f"Processing: {file}")

    path = os.path.join(folder, file)

    try:
        reader = PdfReader(path)
    except Exception as e:
        print(f"Skipping {file}, couldn't read PDF: {e}")
        continue

    # Extract text
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "

    if not text.strip():
        print(f"No text extracted from: {file}")

    text_lower = text.lower()

    # -------------------------
    # Extract date
    # -------------------------
    date_part = extract_date(text)

    # -------------------------
    # Vendor detection
    # -------------------------
    vendor_found = "Unknown"
    for v in vendors:
        if v.lower() in text_lower:
            vendor_found = v.replace(" ", "")
            break

    vendor_found = clean_filename(vendor_found)

    # -------------------------
    # Keyword detection
    # -------------------------
    found_keywords = []
    for key, terms in keywords_map.items():
        if any(term in text_lower for term in terms):
            found_keywords.append(key)

    keyword_part = "-".join(found_keywords[:3]) if found_keywords else "misc"

    # -------------------------
    # Extract "X of:" phrase
    # -------------------------
    phrase_part = "nophrase"

    match = re.search(r'\d+\s+of:\s*(.+)', text, re.IGNORECASE)
    if match:
        following_text = match.group(1)

        # Stop at newline if present
        following_text = following_text.split("\n")[0]

        words = following_text.split()
        first_four = words[:4]

        phrase_part = "-".join(first_four)
        phrase_part = clean_filename(phrase_part)

    # -------------------------
    # Build filename
    # -------------------------
    base_name = f"{date_part}_{vendor_found}_{keyword_part}_{phrase_part}"
    base_name = clean_filename(base_name)
    base_name = base_name[:120]

    # Prevent totally identical generic names
    if base_name == "nodate_Unknown_misc_nophrase":
        base_name += "_" + file.replace(".pdf", "")

    new_name = base_name + ".pdf"
    new_path = os.path.join(folder, new_name)

    # -------------------------
    # Avoid overwriting files
    # -------------------------
    counter = 1
    while os.path.exists(new_path):
        new_name = f"{base_name}_{counter}.pdf"
        new_path = os.path.join(folder, new_name)
        counter += 1

    # -------------------------
    # Rename file
    # -------------------------
    os.rename(path, new_path)
    print(f"Renamed: {file} → {new_name}")
