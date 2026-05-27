


import os
import re
import sys
import shutil
import subprocess
from datetime import datetime
from pypdf import PdfReader

# -------------------------
# FOLDERS
# -------------------------
input_folder = r"\\nu\GIS\Scripts\pdf-rename-test\test"
ocr_folder = r"\\nu\GIS\Scripts\pdf-rename-test\test-ocr-output"

os.makedirs(ocr_folder, exist_ok=True)

# -------------------------
# CONFIG
# -------------------------
vendors = [
    "Amazon", "AMZN", "Amazon.com", "Amazon Services",
    "Home Depot", "Homedepot",
    "Staples",
    "Grainger"
]

keywords_map = {
    "lumber": ["2x4", "plywood", "board"],
    "network": ["ethernet", "switch", "router"],
    "office": ["paper", "pens", "notebook"],
    "lighting": ["led", "light", "lamp"],
    "power": ["inverter", "battery", "generator", "sine"]
}

date_labels = [
    "Order Placed:",
    "Order Date:",
    "Invoice Date:",
    "Purchase Date:",
    "Transaction Date:",
    "Date Purchased:",
    "Submitted:"
]

# -------------------------
# HELPERS
# -------------------------
def clean_filename(s):
    # Keep spaces out of names; allow letters, numbers, dashes, underscores
    return "".join(c for c in s if c.isalnum() or c in ("-", "_"))

def extract_date(text):
    for label in date_labels:
        # Example: January 20, 2026
        pattern1 = rf'{re.escape(label)}\s*([A-Za-z]+ \d{{1,2}}, \d{{4}})'
        m1 = re.search(pattern1, text, re.IGNORECASE)
        if m1:
            try:
                dt = datetime.strptime(m1.group(1), "%B %d, %Y")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

        # Example: 01/20/2026
        pattern2 = rf'{re.escape(label)}\s*(\d{{2}}/\d{{2}}/\d{{4}})'
        m2 = re.search(pattern2, text, re.IGNORECASE)
        if m2:
            try:
                dt = datetime.strptime(m2.group(1), "%m/%d/%Y")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

    return "nodate"

def extract_phrase(text):
    # Primary pattern: "3 of: item description here"
    match = re.search(r'\d+\s+of:\s*(.+)', text, re.IGNORECASE)
    if match:
        line = match.group(1).split("\n")[0].strip()
        words = line.split()
        if words:
            return "-".join(words[:4])

    # Fallback: first line with at least 4 words
    for line in text.splitlines():
        words = line.strip().split()
        if len(words) >= 4:
            return "-".join(words[:4])

    return "nophrase"

# -------------------------
# DIAGNOSTICS
# -------------------------
print("Python executable:", sys.executable)
print("ocrmypdf on PATH:", shutil.which("ocrmypdf"))
print("tesseract on PATH:", shutil.which("tesseract"))
print("gswin64c on PATH:", shutil.which("gswin64c"))
print(f"Input folder exists: {os.path.isdir(input_folder)}")
print(f"OCR folder exists:   {os.path.isdir(ocr_folder)}")
print("-" * 60)

# -------------------------
# STEP 1: OCR PDFs
# -------------------------
files = list(os.listdir(input_folder))

for file in files:
    if not file.lower().endswith(".pdf"):
        continue

    # Skip already-processed style names
    if file.startswith("nodate_") or re.match(r"\d{4}-\d{2}-\d{2}_", file):
        print(f"Skipping already processed file: {file}")
        continue

    input_path = os.path.join(input_folder, file)
    output_path = os.path.join(ocr_folder, file)

    if not os.path.isfile(input_path):
        print(f"Missing input file: {input_path}")
        continue

    print(f"OCR processing: {file}")
    print(f"  Input : {input_path}")
    print(f"  Output: {output_path}")

    try:
        # Use the SAME Python interpreter currently running this script
        cmd = [
            sys.executable,
            "-m",
            "ocrmypdf",
            "--skip-text",
            "--invalidate-digital-signatures",
            input_path,
            output_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        print("  Return code:", result.returncode)

        if result.stdout.strip():
            print("  STDOUT:")
            print(result.stdout)

        if result.stderr.strip():
            print("  STDERR:")
            print(result.stderr)

        if result.returncode != 0:
            print(f"❌ OCR FAILED for {file}")
            continue

        if not os.path.exists(output_path):
            print(f"❌ OCR reported success, but output file not found: {output_path}")
            continue

        print(f"✅ OCR complete: {file}")

    except FileNotFoundError as e:
        print(f"❌ Subprocess failed before OCR started: {e}")
        print("This usually means VS Code cannot find the executable/module environment.")
        continue
    except Exception as e:
        print(f"❌ Unexpected OCR exception for {file}: {e}")
        continue

# -------------------------
# STEP 2: RENAME OCR FILES
# -------------------------
ocr_files = list(os.listdir(ocr_folder))

for file in ocr_files:
    if not file.lower().endswith(".pdf"):
        continue

    path = os.path.join(ocr_folder, file)
    print(f"Processing OCR file: {file}")

    try:
        reader = PdfReader(path)
    except Exception as e:
        print(f"Skipping unreadable PDF: {file} ({e})")
        continue

    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    if not text.strip():
        print(f"No text found after OCR: {file}")
        continue

    text_lower = text.lower()

    # Date
    date_part = extract_date(text)

    # Vendor
    vendor_found = "Unknown"
    for v in vendors:
        if v.lower() in text_lower:
            vendor_found = v.replace(" ", "")
            break
    vendor_found = clean_filename(vendor_found)

    # Keywords
    found_keywords = []
    for key, terms in keywords_map.items():
        if any(term.lower() in text_lower for term in terms):
            found_keywords.append(key)

    keyword_part = "-".join(found_keywords[:3]) if found_keywords else "misc"

    # Phrase
    phrase_part = clean_filename(extract_phrase(text))

    # Build filename
    base_name = f"{date_part}_{vendor_found}_{keyword_part}_{phrase_part}"
    base_name = clean_filename(base_name)
    base_name = base_name[:120]

    # Skip low-confidence junk names
    if base_name == "nodate_Unknown_misc_nophrase":
        print(f"Skipping low-confidence file: {file}")
        continue

    new_name = base_name + ".pdf"
    new_path = os.path.join(ocr_folder, new_name)

    # Prevent overwrites
    counter = 1
    while os.path.exists(new_path) and os.path.abspath(new_path) != os.path.abspath(path):
        new_name = f"{base_name}_{counter}.pdf"
        new_path = os.path.join(ocr_folder, new_name)
        counter += 1

    # If renamed name is different, rename
    if os.path.abspath(new_path) != os.path.abspath(path):
        os.rename(path, new_path)
        print(f"Renamed → {new_name}")
    else:
        print(f"Already correctly named: {file}")