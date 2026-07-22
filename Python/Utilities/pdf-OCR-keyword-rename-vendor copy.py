


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
log_file = os.path.join(ocr_folder+"\logs", f"rename_log_{run_timestamp}.csv")

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
    "safety": ["glove", "goggles", "helmet", "vest", "boots"],
    "industrial": ["industrial", "distributor", "tariff", "assembly", "kit"],
    "vehicle": ["truck", "vehicle", "crew", "toolbox", "maintenance"]
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
            r"Order Date:\s*(\d{2}/\d{2}/\d{4})"
        ],
        "keywords": {
            "lighting": ["led", "lamp", "fixture", "shop light", "bulb", "floodlight"],
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
        "date_strategy": "pattern_list",
        "description_strategy": "amazon"
    },

    "TipcoTechnologies": {
        "markers": [
            "tipcotech.com",
            "tipco",
            "owings mills",
            "cronhill",
        ],
        "date_patterns": [
            r"Invoice Date[:\s]+(\d{2}/\d{2}/\d{4})", # some variations have different spacing
            r"Invoice\s*Date\s+(\d{2}/\d{2}/\d{4})", # some variations have different spacing
            r"Order Date[:\s]+(\d{2}/\d{2}/\d{4})" # standard MM/DD/YYYY format
        ],
        "keywords": {
            "inventory": ["hose", "jacket", "double jacket", "coupling", "fitting", "valve", "pump"],
            "industrial": ["tipco", "industrial", "import", "tariff", "distributor"],
            "vehicle": ["truck", "vehicle", "crew", "tools"], 
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
        "date_strategy": "pattern_list",
        "description_strategy": "table_basic"
    },
    
    "Furguson": {
        "markers": [
            "4156 S. MILITARY HIGHWAY",
            "407-816-6550"
        ],
        "date_patterns": [
            r"Invoice Date[:\s]+(\d{2}/\d{2}/\d{4})" # standard MM/DD/YYYY format
        ],
        "keywords": {
            "industrial": ["clmp", "coup", "sdl", "tracer box lid", "tracer box clamp", "tracer box coupling", 
                           "tracer box saddle", "tracer box repair kit", "DI MJ WDG REST GLND", "MJ C153 90 BEND",
                           "PNT SAN ANGELO DIGGING BAR", "yoke"]
        },
        "ignore_terms": [
            "job name",
            "tax code",
            "CUSTOMER ORDER NUMBER",
            "ITEM NUMBER",
            "lead law warning",
            "non-potable",
            "buyer is solely responsible",
            "not lead free",
            "anticipated for human consumption",
            "invoice sub-total",
            "approved",
            "remit to change",     
            "lead law warning",
            "non-potable",
            "buyer is solely responsible",
            "not lead free"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": "table_basic"
    },
    "CMC_Supply": {
        "markers": [
            "cmc supply",
            "2510 johnson ave nw",
            "cmc",
            "invoice date",
            "po box 12058"
        ],
        "date_patterns": [
            r"INVOICE DATE:\s*([A-Za-z]+ \d{1,2}, \d{4})",
            r"Order Date:\s*([A-Za-z]+ \d{1,2}, \d{4})",
            r"Order Placed:\s*(\d{2}/\d{2}/\d{4})",
        ],
        "keywords": {
            "meter": ["lid", "box", "sdr26", "diameter", "meter", "fitting"],
            "pipe": ["sdr26", "diameter", "fitting", "pvc", "ductile"],
            "office": ["paper", "toner", "pen", "notebook"],
            "tools": ["drill", "saw", "socket", "wrench", "driver"]
        },
        "ignore_terms": [
            "ot our truck",
            "ship date",
            "unit price",
            "writer",
            "unit price,"
            "ext price"

        ],
        "description_strategy": "table_basic"
    },

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
# HELPERS
# ============================================================
def clean_filename(text):
    return "".join(c for c in text if c.isalnum() or c in ("-", "_"))

def parse_date_string(raw):
    raw = raw.strip()
    date_formats = [
        "%B %d, %Y",   # January 20, 2026
        "%m/%d/%Y",    # 02/06/2026
        "%m-%d-%Y",    # 02-06-2026
        "%Y-%m-%d",    # 2026-02-06
        "%m/%d/%y"     # 02/06/26
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
    return bool(re.fullmatch(r"[\d\.\,\$\-\s/]+", line.strip()))

def contains_ignore_term(line, ignore_terms):
    line_lower = line.lower()
    return any(term.lower() in line_lower for term in ignore_terms)

def clean_description_tokens(text, max_words=6):
    words = text.replace("/", " ").split()
    words = [clean_filename(w) for w in words]
    words = [w for w in words if w]
    return "-".join(words[:max_words]) if words else "nophrase"

def get_profile(vendor_name):
    return VENDOR_PROFILES.get(vendor_name, {})

def get_ignore_terms(vendor_name):
    ignore_terms = GENERIC_IGNORE_TERMS.copy()
    profile = get_profile(vendor_name)
    ignore_terms.extend(profile.get("ignore_terms", []))
    return ignore_terms

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

    return best_vendor if best_score > 0 else "Unknown"

# ============================================================
# DATE STRATEGIES
# ============================================================
def extract_date_generic(text, vendor_name=None):
    # First: try generic labeled date patterns
    for label in GENERIC_DATE_LABELS:
        pattern1 = rf"{re.escape(label)}\s*([A-Za-z]+ \d{{1,2}}, \d{{4}})"
        m1 = re.search(pattern1, text, re.IGNORECASE)
        if m1:
            return parse_date_string(m1.group(1))

        pattern2 = rf"{re.escape(label)}\s*(\d{{2}}/\d{{2}}/\d{{4}})"
        m2 = re.search(pattern2, text, re.IGNORECASE)
        if m2:
            return parse_date_string(m2.group(1))

    # Second: generic free-form date search
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

def extract_date_from_profile_patterns(text, vendor_name):
    profile = get_profile(vendor_name)
    for pattern in profile.get("date_patterns", []):
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            parsed = parse_date_string(m.group(1))
            if parsed != "nodate":
                return parsed

    # fallback to generic if vendor patterns fail
    return extract_date_generic(text, vendor_name)

DATE_STRATEGIES = {
    "generic": extract_date_generic,
    "pattern_list": extract_date_from_profile_patterns
}

def extract_date(text, vendor_name):
    strategy = "generic"
    profile = get_profile(vendor_name)
    strategy = profile.get("date_strategy", "generic")

    extractor = DATE_STRATEGIES.get(strategy, extract_date_generic)
    return extractor(text, vendor_name)

# ============================================================
# CATEGORY / KEYWORD EXTRACTION
# ============================================================
def extract_category(text, vendor_name):
    text_lower = text.lower()

    profile = get_profile(vendor_name)
    vendor_keywords = profile.get("keywords", {})

    for category, terms in vendor_keywords.items():
        for term in terms:
            if term.lower() in text_lower:
                return category

    for category, terms in GENERIC_KEYWORDS.items():
        for term in terms:
            if term.lower() in text_lower:
                return category

    return "misc"

# ============================================================
# DESCRIPTION STRATEGY HELPERS
# ============================================================
def score_candidate_line(line, ignore_terms):
    score = 0
    line_strip = line.strip()

    if len(line_strip) < 4:
        return -999

    if is_mostly_numeric_or_price(line_strip):
        return -999

    if contains_ignore_term(line_strip, ignore_terms):
        return -999

    if re.search(r"[A-Za-z]", line_strip):
        score += 2

    if re.search(r"[A-Za-z]", line_strip) and re.search(r"\d", line_strip):
        score += 3

    if 8 <= len(line_strip) <= 80:
        score += 2

    if line_strip.lower().startswith(("bill to", "ship to", "invoice", "customer", "branch")):
        score -= 5

    if re.search(r"\$\s*\d", line_strip):
        score -= 3

    return score

# ============================================================
# DESCRIPTION STRATEGIES
# ============================================================
def extract_description_table_basic(text, vendor_name):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    ignore_terms = get_ignore_terms(vendor_name)

    # Common table header keywords
    header_keywords = [
        "description",
        "item description",
        "item",
        "product",
        "qty",
        "quantity",
        "unit price",
        "extended price",
        "amount",
        "uom",
        "sku"
    ]

    # Try to locate the table header region
    header_index = None
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if sum(1 for keyword in header_keywords if keyword in line_lower) >= 2:
            header_index = i
            break

    # If no obvious header found, fall back to generic extraction
    if header_index is None:
        return extract_description_generic(text, vendor_name)

    # Look at the next several lines after the header
    candidate_lines = lines[header_index + 1: header_index + 20]

    # Helper to trim trailing price-like tokens
    def strip_trailing_price_tokens(line):
        tokens = line.split()

        # Remove obvious trailing numeric/price tokens from the end
        while tokens:
            last = tokens[-1]
            if re.fullmatch(r"[\$]?\d[\d,]*\.?\d*", last) or re.fullmatch(r"\d+\.\d{2}", last):
                tokens.pop()
            else:
                break

        return " ".join(tokens)

    # Score candidate lines
    scored = []
    for idx, line in enumerate(candidate_lines):
        line_clean = strip_trailing_price_tokens(line)

        if not line_clean.strip():
            continue

        s = score_candidate_line(line_clean, ignore_terms)

        # Bonus if line is shortly after the header
        if idx < 6:
            s += 2

        # Bonus if line contains letters and numbers (common for item rows / SKUs)
        if re.search(r"[A-Za-z]", line_clean) and re.search(r"\d", line_clean):
            s += 2

        # Penalty if line looks like a total/tax row
        if re.search(r"\b(total|subtotal|tax|amount due)\b", line_clean, re.IGNORECASE):
            s -= 10

        if s > 0:
            scored.append((s, idx, line_clean))

    # If nothing strong found, fall back
    if not scored:
        return extract_description_generic(text, vendor_name)

    # Pick best candidate
    scored.sort(reverse=True, key=lambda x: x[0])
    best_score, best_idx, best_line = scored[0]

    combined = best_line

    # Optional continuation line
    if best_idx + 1 < len(candidate_lines):
        next_line = candidate_lines[best_idx + 1].strip()

        if next_line:
            next_line_clean = strip_trailing_price_tokens(next_line)

            if (
                not contains_ignore_term(next_line_clean, ignore_terms)
                and not is_mostly_numeric_or_price(next_line_clean)
                and len(next_line_clean.split()) >= 2
                and not re.search(r"\b(total|subtotal|tax|amount due)\b", next_line_clean, re.IGNORECASE)
            ):
                combined = f"{best_line} {next_line_clean}"

    return clean_description_tokens(combined, max_words=8)

def extract_description_generic(text, vendor_name):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    ignore_terms = get_ignore_terms(vendor_name)

    label_patterns = [
        r"Description[:\s]+(.+)",
        r"Item[:\s]+(.+)",
        r"Product[:\s]+(.+)"
    ]
    for pattern in label_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return clean_description_tokens(m.group(1), max_words=6)

    scored = []
    for line in lines:
        s = score_candidate_line(line, ignore_terms)
        if s > 0:
            scored.append((s, line))

    if scored:
        scored.sort(reverse=True, key=lambda x: x[0])
        return clean_description_tokens(scored[0][1], max_words=6)

    return "nophrase"

def extract_description_amazon(text, vendor_name):
    match = re.search(r"\d+\s+of:\s*(.+)", text, re.IGNORECASE)
    if match:
        line = match.group(1).split("\n")[0].strip()
        return clean_description_tokens(line, max_words=6)

    return extract_description_generic(text, vendor_name)

def extract_description_tipco(text, vendor_name):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    ignore_terms = get_ignore_terms(vendor_name)

    # Try item description section first
    header_index = None
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if ("item description" in line_lower) or ("item id" in line_lower and "description" in line_lower):
            header_index = i
            break

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
        
def extract_description_ferguson(text, vendor_name):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    ignore_terms = get_ignore_terms(vendor_name)

    # Find the invoice item table header
    header_index = None
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if "item number" in line_lower and "description" in line_lower:
            header_index = i
            break

    if header_index is None:
        return extract_description_table_basic(text, vendor_name)

    candidate_lines = lines[header_index + 1: header_index + 8]

    def strip_leading_row_fields(line):
        # Remove leading quantity / shipped / item number patterns
        # Example OCR line might look like:
        # 2 2 RCB6304 6X8-12 SWR SDL 6.28-6.30 216.415 EA 432.83
        line = re.sub(r'^\s*\d+\s+\d+\s+[A-Z0-9-]+\s+', '', line)
        return line

    def strip_trailing_price_fields(line):
        # Remove trailing "216.415 EA 432.83" style fields
        line = re.sub(r'\s+\d+(?:\.\d+)?\s+[A-Z]{1,3}\s+\d+(?:\.\d+)?\s*$', '', line)
        return line

    scored = []
    for idx, line in enumerate(candidate_lines):
        if contains_ignore_term(line, ignore_terms):
            continue

        candidate = strip_leading_row_fields(line)
        candidate = strip_trailing_price_fields(candidate)
        candidate = candidate.strip()

        if not candidate:
            continue

        if is_mostly_numeric_or_price(candidate):
            continue

        score = 0

        # Strong bonus for being right after the header
        if idx < 3:
            score += 6

        # Bonus for mixed letters/numbers (common in item descriptions)
        if re.search(r"[A-Za-z]", candidate) and re.search(r"\d", candidate):
            score += 4

        # Penalize warning/legal language
        if re.search(r"(non-potable|lead law warning|buyer is solely responsible|not lead free)", candidate, re.IGNORECASE):
            score -= 20

        # Bonus for sewer/waterworks terms
        if re.search(r"(swr|saddle|sewer|pipe|romac)", candidate, re.IGNORECASE):
            score += 4

        if score > 0:
            scored.append((score, candidate))

    if scored:
        scored.sort(reverse=True, key=lambda x: x[0])
        return clean_description_tokens(scored[0][1], max_words=8)

    return extract_description_table_basic(text, vendor_name)


    # Fallback: global best candidate line
    scored = []
    for line in lines:
        s = score_candidate_line(line, ignore_terms)
        if s > 0:
            scored.append((s, line))

    if scored:
        scored.sort(reverse=True, key=lambda x: x[0])
        return clean_description_tokens(scored[0][1], max_words=8)

    return "nophrase"

DESCRIPTION_STRATEGIES = {
    "generic": extract_description_generic,
    "amazon": extract_description_amazon,
    "tipco": extract_description_tipco,
    "table_basic": extract_description_table_basic,
    "ferguson": extract_description_ferguson
}

def extract_description(text, vendor_name):
    strategy = "generic"
    profile = get_profile(vendor_name)
    strategy = profile.get("description_strategy", "generic")

    extractor = DESCRIPTION_STRATEGIES.get(strategy, extract_description_generic)
    return extractor(text, vendor_name)

# ============================================================
# OCR STEP
# ============================================================
def run_ocr():
    files = list(os.listdir(input_folder))
    pdf_files = [f for f in files if f.lower().endswith(".pdf")]

    print(f"Found {len(pdf_files)} PDF file(s) in input folder.")

    for file in pdf_files:
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

        # keep newlines for line-based parsing; just normalize spaces/tabs
        text = re.sub(r"[ \t]+", " ", text)

        vendor_name = detect_vendor(text)
        safe_vendor = clean_filename(vendor_name) if vendor_name != "Unknown" else "Unknown"

        date_part = extract_date(text, vendor_name)
        category = extract_category(text, vendor_name)
        description = extract_description(text, vendor_name)
        description = clean_filename(description)

        base_name = f"{date_part}_{safe_vendor}_{category}_{description}"
        base_name = clean_filename(base_name)
        base_name = base_name[:140]

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
    print("-" * 70)

    run_ocr()
    rename_ocr_files()

    print("\nDone.")
    print(f"Log written to: {log_file}")

if __name__ == "__main__":
    main()
