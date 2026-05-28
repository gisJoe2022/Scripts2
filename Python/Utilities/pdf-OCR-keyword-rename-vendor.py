

import os
import re
import sys
import csv
import shutil
import subprocess
from datetime import datetime
from pypdf import PdfReader

# ============================================================
# FOLDERS
# ============================================================
input_folder = r"\\nu\GIS\Scripts\pdf-rename-test\test"
ocr_folder = r"\\nu\GIS\Scripts\pdf-rename-test\test-ocr-output"

os.makedirs(ocr_folder, exist_ok=True)

# Timestamped CSV log
run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(ocr_folder, f"rename_log_{run_timestamp}.csv")

# ============================================================
# GLOBAL GENERIC CONFIG
# ============================================================
GENERIC_DATE_LABELS = [
    "Order Placed:",
    "Order Date:",
    "Invoice Date:",
    "Purchase Date:",
    "Transaction Date:",
    "Date Purchased:",
    "Submitted:",
    "Date:"
]

GENERIC_KEYWORDS = {
    "lumber": ["2x4", "plywood", "board", "framing", "decking"],
    "network": ["ethernet", "switch", "router", "cat5", "cat6", "patch cable"],
    "office": ["paper", "pens", "notebook", "binder", "copy paper", "toner"],
    "lighting": ["led", "light", "lamp", "fixture", "shop light", "bulb"],
    "power": ["inverter", "battery", "generator", "charger", "sine"],
    "hose": ["hose", "jacket", "coupling", "fitting", "valve", "pump", "hydraulic"],
    "safety": ["glove", "goggles", "helmet", "vest", "boots"]
}

GENERIC_IGNORE_TERMS = [
    "subtotal", "tax", "total", "balance", "invoice", "bill to", "ship to",
    "payment", "terms", "tracking", "order summary", "thank you", "account",
    "customer", "page", "amount due", "discount", "approved", "carrier",
    "branch", "customer id", "po number", "net due date", "disc due date",
    "unit price", "extended price", "pricing", "uom", "quantities"
]

# ============================================================
# VENDOR PROFILES
# ============================================================
VENDOR_PROFILES = {
    "Amazon": {
        "markers": [
            "amazon.com",
            "amazon services",
            "amzn",
            "order placed",
            "sold by amazon"
        ],
        "date_patterns": [
            r"Order Placed:\s*([A-Za-z]+ \d{1,2}, \d{4})",
            r"Order Date:\s*([A-Za-z]+ \d{1,2}, \d{4})",
            r"Order Placed:\s*(\d{2}/\d{2}/\d{4})",
        ],
        "keywords": {
            "lighting": ["led", "shop light", "fixture", "lamp", "light"],
            "power": ["inverter", "battery", "charger", "generator", "sine"],
            "network": ["ethernet", "cat6", "cat5", "switch", "router"],
            "office": ["paper", "toner", "pen", "notebook"],
            "tools": ["drill", "saw", "socket", "wrench", "driver"]
        },
        "ignore_terms": [
            "return window",
            "ship to",
            "payment method",
            "order summary"
        ],
        "description_strategy": "amazon"
    },

    "TipcoTechnologies": {
        "markers": [
            "tipcotech.com",
            "tipco",
            "owings mills",
            "cronhill",
            "invoice date",
            "order number"
        ],
        "date_patterns": [
            r"Invoice Date[:\s]+(\d{2}/\d{2}/\d{4})",
            r"Invoice\s*Date\s+(\d{2}/\d{2}/\d{4})",
            r"Order Date[:\s]+(\d{2}/\d{2}/\d{4})"
        ],
        "keywords": {
            "hose": ["hose", "jacket", "double jacket", "coupling", "fitting", "valve", "pump"],
            "industrial": ["tipco", "industrial", "import", "tariff", "distributor"],
            "vehicle": ["truck", "vehicle", "crew", "tools"]
        },
        "ignore_terms": [
            "approved",
            "please email",
            "carrier",
            "tracking #",
            "invoice date",
            "ship to",
            "bill to",
            "branch",
            "order number",
            "customer id",
            "customer fulfillment member",
            "pricing uom",
            "extended price",
            "unit price",
            "discount amount",
            "original"
        ],
        "description_strategy": "tipco"
    }
}

# ============================================================
# LOGGING
# ============================================================
def ensure_log_file(path):
    with open(path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "stage",
            "source_file",
            "ocr_file",
            "final_file",
            "status",
            "vendor",
            "date",
            "category",
            "description",
            "notes"
        ])

def write_log(stage, source_file="", ocr_file="", final_file="", status="", vendor="",
              date_part="", category="", description="", notes=""):
    with open(log_file, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            stage,
            source_file,
            ocr_file,
            final_file,
            status,
            vendor,
            date_part,
            category,
            description,
            notes
        ])

# ============================================================
# TEXT / FILENAME HELPERS
# ============================================================
def clean_filename(text):
    return "".join(c for c in text if c.isalnum() or c in ("-", "_"))

def normalize_spaces(text):
    return re.sub(r"\s+", " ", text).strip()

def parse_date_string(raw):
    raw = raw.strip()
    date_formats = [
        "%B %d, %Y",   # January 20, 2026
        "%m/%d/%Y",    # 02/06/2026
        "%m-%d-%Y",
        "%Y-%m-%d"
    ]
    for fmt in date_formats:
        try:
            dt = datetime.strptime(raw, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return "nodate"

def is_mostly_numeric_or_price(line):
    if not line.strip():
        return True
    if re.fullmatch(r"[\d\.\,\$\-\s/]+", line.strip()):
        return True
    return False

def contains_ignore_term(line, ignore_terms):
    line_lower = line.lower()
    return any(term.lower() in line_lower for term in ignore_terms)

def clean_description_tokens(text, max_words=6):
    words = text.replace("/", " ").split()
    words = [clean_filename(w) for w in words]
    words = [w for w in words if w]
    return "-".join(words[:max_words]) if words else "nophrase"

# ============================================================
# VENDOR DETECTION
# ============================================================
def detect_vendor(text):
    text_lower = text.lower()
    best_vendor = "Unknown"
    best_score = 0

    for vendor_name, profile in VENDOR_PROFILES.items():
        score = 0
        for marker in profile.get("markers", []):
            if marker.lower() in text_lower:
                score += 1

        if score > best_score:
            best_score = score
            best_vendor = vendor_name

    # Require at least one marker hit
    if best_score == 0:
        return "Unknown"

    return best_vendor

# ============================================================
# DATE EXTRACTION
# ============================================================
def extract_date_generic(text):
    # First try labeled patterns
    for label in GENERIC_DATE_LABELS:
        pattern1 = rf"{re.escape(label)}\s*([A-Za-z]+ \d{{1,2}}, \d{{4}})"
        m1 = re.search(pattern1, text, re.IGNORECASE)
        if m1:
            return parse_date_string(m1.group(1))

        pattern2 = rf"{re.escape(label)}\s*(\d{{2}}/\d{{2}}/\d{{4}})"
        m2 = re.search(pattern2, text, re.IGNORECASE)
        if m2:
            return parse_date_string(m2.group(1))

    # Then try generic date search
    generic_patterns = [
        r"([A-Za-z]+ \d{1,2}, \d{4})",
        r"(\d{2}/\d{2}/\d{4})",
        r"(\d{4}-\d{2}-\d{2})"
    ]
    for pattern in generic_patterns:
        m = re.search(pattern, text)
        if m:
            parsed = parse_date_string(m.group(1))
            if parsed != "nodate":
                return parsed

    return "nodate"

def extract_date_for_vendor(text, vendor_name):
    if vendor_name in VENDOR_PROFILES:
        for pattern in VENDOR_PROFILES[vendor_name].get("date_patterns", []):
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                parsed = parse_date_string(m.group(1))
                if parsed != "nodate":
                    return parsed

    return extract_date_generic(text)

# ============================================================
# CATEGORY / KEYWORD EXTRACTION
# ============================================================
def extract_category(text, vendor_name):
    text_lower = text.lower()

    # Vendor-specific keywords first
    if vendor_name in VENDOR_PROFILES:
        keywords = VENDOR_PROFILES[vendor_name].get("keywords", {})
        for category, terms in keywords.items():
            for term in terms:
                if term.lower() in text_lower:
                    return category

    # Global fallback
    for category, terms in GENERIC_KEYWORDS.items():
        for term in terms:
            if term.lower() in text_lower:
                return category

    return "misc"

# ============================================================
# DESCRIPTION EXTRACTION
# ============================================================
def extract_description_amazon(text, vendor_name):
    # Look for "X of: <item description>"
    match = re.search(r"\d+\s+of:\s*(.+)", text, re.IGNORECASE)
    if match:
        line = match.group(1).split("\n")[0].strip()
        return clean_description_tokens(line, max_words=6)

    # Fallback: first reasonable line
    return extract_description_generic(text, vendor_name)

def score_candidate_line(line, ignore_terms):
    score = 0
    line_strip = line.strip()

    if len(line_strip) < 4:
        return -999

    if is_mostly_numeric_or_price(line_strip):
        return -999

    if contains_ignore_term(line_strip, ignore_terms):
        return -999

    # Prefer lines with letters
    if re.search(r"[A-Za-z]", line_strip):
        score += 2

    # Prefer lines with letters + digits (often useful product identifiers)
    if re.search(r"[A-Za-z]", line_strip) and re.search(r"\d", line_strip):
        score += 3

    # Prefer medium length descriptive lines
    if 8 <= len(line_strip) <= 80:
        score += 2

    # Penalize lines that are probably addresses or headers
    if line_strip.lower().startswith(("bill to", "ship to", "invoice", "customer", "branch")):
        score -= 5

    # Penalize obvious money patterns
    if re.search(r"\$\s*\d", line_strip):
        score -= 3

    return score

def extract_description_tipco(text, vendor_name):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    ignore_terms = GENERIC_IGNORE_TERMS.copy()
    if vendor_name in VENDOR_PROFILES:
        ignore_terms.extend(VENDOR_PROFILES[vendor_name].get("ignore_terms", []))

    # 1) Try to find the item description section
    header_index = None
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if ("item description" in line_lower) or ("item id" in line_lower and "description" in line_lower):
            header_index = i
            break

    # If found, search the next several lines for the best descriptive candidate
    if header_index is not None:
        candidate_lines = lines[header_index + 1: header_index + 15]

        scored = []
        for line in candidate_lines:
            s = score_candidate_line(line, ignore_terms)
            if s > 0:
                scored.append((s, line))

        if scored:
            scored.sort(reverse=True, key=lambda x: x[0])
            best_line = scored[0][1]

            # Possible continuation line
            best_index = candidate_lines.index(best_line)
            combined = best_line

            if best_index + 1 < len(candidate_lines):
                next_line = candidate_lines[best_index + 1]
                if (
                    not contains_ignore_term(next_line, ignore_terms)
                    and not is_mostly_numeric_or_price(next_line)
                    and len(next_line.split()) >= 2
                ):
                    combined = f"{best_line} {next_line}"

            return clean_description_tokens(combined, max_words=8)

    # 2) Secondary fallback: scan whole document for descriptive product-like lines
    scored = []
    for line in lines:
        s = score_candidate_line(line, ignore_terms)
        if s > 0:
            scored.append((s, line))

    if scored:
        scored.sort(reverse=True, key=lambda x: x[0])
        return clean_description_tokens(scored[0][1], max_words=8)

    # 3) Final fallback
    return "nophrase"

def extract_description_generic(text, vendor_name):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    ignore_terms = GENERIC_IGNORE_TERMS.copy()
    if vendor_name in VENDOR_PROFILES:
        ignore_terms.extend(VENDOR_PROFILES[vendor_name].get("ignore_terms", []))

    # Look for labeled fields first
    label_patterns = [
        r"Description[:\s]+(.+)",
        r"Item[:\s]+(.+)",
        r"Product[:\s]+(.+)"
    ]
    for pattern in label_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return clean_description_tokens(m.group(1), max_words=6)

    # Score all lines and take best candidate
    scored = []
    for line in lines:
        s = score_candidate_line(line, ignore_terms)
        if s > 0:
            scored.append((s, line))

    if scored:
        scored.sort(reverse=True, key=lambda x: x[0])
        return clean_description_tokens(scored[0][1], max_words=6)

    return "nophrase"

def extract_description(text, vendor_name):
    strategy = None
    if vendor_name in VENDOR_PROFILES:
        strategy = VENDOR_PROFILES[vendor_name].get("description_strategy")

    if strategy == "amazon":
        return extract_description_amazon(text, vendor_name)
    elif strategy == "tipco":
        return extract_description_tipco(text, vendor_name)
    else:
        return extract_description_generic(text, vendor_name)

# ============================================================
# OCR STEP
# ============================================================
def run_ocr():
    files = list(os.listdir(input_folder))
    pdf_files = [f for f in files if f.lower().endswith(".pdf")]

    print(f"Found {len(pdf_files)} PDF file(s) in input folder.")

    for file in pdf_files:
        # Skip files that already look renamed
        if file.startswith("nodate_") or re.match(r"\d{4}-\d{2}-\d{2}_", file):
            print(f"Skipping already processed file: {file}")
            write_log(
                stage="ocr",
                source_file=file,
                status="skipped",
                notes="Filename already appears processed"
            )
            continue

        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(ocr_folder, file)

        if not os.path.isfile(input_path):
            print(f"Missing input file: {input_path}")
            write_log(
                stage="ocr",
                source_file=file,
                status="error",
                notes=f"Missing input file: {input_path}"
            )
            continue

        print(f"\nOCR processing: {file}")
        print(f"  Input : {input_path}")
        print(f"  Output: {output_path}")

        try:
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

            if result.stderr.strip():
                print("  STDERR:")
                print(result.stderr)

            if result.returncode != 0:
                write_log(
                    stage="ocr",
                    source_file=file,
                    ocr_file=os.path.basename(output_path),
                    status="failed",
                    notes=result.stderr.strip() if result.stderr.strip() else "OCR failed"
                )
                continue

            if not os.path.exists(output_path):
                write_log(
                    stage="ocr",
                    source_file=file,
                    ocr_file=os.path.basename(output_path),
                    status="failed",
                    notes="OCR reported success, but output file not found"
                )
                continue

            write_log(
                stage="ocr",
                source_file=file,
                ocr_file=os.path.basename(output_path),
                status="success",
                notes="OCR completed successfully"
            )

        except Exception as e:
            write_log(
                stage="ocr",
                source_file=file,
                ocr_file=os.path.basename(output_path),
                status="error",
                notes=f"OCR exception: {e}"
            )

# ============================================================
# RENAME STEP
# ============================================================
def rename_ocr_files():
    ocr_files = list(os.listdir(ocr_folder))
    ocr_pdf_files = [f for f in ocr_files if f.lower().endswith(".pdf")]

    print(f"\nFound {len(ocr_pdf_files)} PDF file(s) in OCR folder.")

    for file in ocr_pdf_files:
        path = os.path.join(ocr_folder, file)
        print(f"\nProcessing OCR file: {file}")

        try:
            reader = PdfReader(path)
        except Exception as e:
            print(f"Unreadable PDF: {file}")
            write_log(
                stage="rename",
                ocr_file=file,
                status="error",
                notes=f"Unreadable PDF: {e}"
            )
            continue

        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        if not text.strip():
            print(f"No text found after OCR: {file}")
            write_log(
                stage="rename",
                ocr_file=file,
                status="skipped",
                notes="No text found after OCR"
            )
            continue

        text = normalize_spaces(text).replace("  ", " ")
        text_lower = text.lower()

        # Detect vendor
        vendor_name = detect_vendor(text)
        safe_vendor = clean_filename(vendor_name) if vendor_name != "Unknown" else "Unknown"

        # Date
        date_part = extract_date_for_vendor(text, vendor_name)

        # Category
        category = extract_category(text, vendor_name)

        # Description
        description = extract_description(text, vendor_name)
        description = clean_filename(description)

        # Final base filename
        base_name = f"{date_part}_{safe_vendor}_{category}_{description}"
        base_name = clean_filename(base_name)
        base_name = base_name[:140]

        # Skip useless names
        if base_name in ("nodate_Unknown_misc_nophrase", "nodate_Unknown_misc_"):
            print(f"Skipping low-confidence file: {file}")
            write_log(
                stage="rename",
                ocr_file=file,
                status="skipped",
                vendor=vendor_name,
                date_part=date_part,
                category=category,
                description=description,
                notes="Low-confidence extraction; rename skipped"
            )
            continue

        new_name = base_name + ".pdf"
        new_path = os.path.join(ocr_folder, new_name)

        # Prevent overwrite collisions
        counter = 1
        while os.path.exists(new_path) and os.path.abspath(new_path) != os.path.abspath(path):
            new_name = f"{base_name}_{counter}.pdf"
            new_path = os.path.join(ocr_folder, new_name)
            counter += 1

        if os.path.abspath(new_path) != os.path.abspath(path):
            os.rename(path, new_path)
            print(f"Renamed → {new_name}")
            write_log(
                stage="rename",
                ocr_file=file,
                final_file=new_name,
                status="renamed",
                vendor=vendor_name,
                date_part=date_part,
                category=category,
                description=description,
                notes="Rename successful"
            )
        else:
            print(f"Already correctly named: {file}")
            write_log(
                stage="rename",
                ocr_file=file,
                final_file=file,
                status="unchanged",
                vendor=vendor_name,
                date_part=date_part,
                category=category,
                description=description,
                notes="Filename already matched desired output"
            )

# ============================================================
# MAIN
# ============================================================
def main():
    ensure_log_file(log_file)

    print("Python executable:", sys.executable)
    print("ocrmypdf on PATH:", shutil.which("ocrmypdf"))
    print("tesseract on PATH:", shutil.which("tesseract"))
    print("gswin64c on PATH:", shutil.which("gswin64c"))
    print(f"Input folder exists: {os.path.isdir(input_folder)}")
    print(f"OCR folder exists:   {os.path.isdir(ocr_folder)}")
    print(f"Log file:            {log_file}")
    print("-" * 65)

    run_ocr()
    rename_ocr_files()

    print("\nDone.")
    print(f"Log written to: {log_file}")

if __name__ == "__main__":
    main()
