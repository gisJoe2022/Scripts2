

import os
import re
import sys
import csv
import shutil
import subprocess
from datetime import datetime
from pypdf import PdfReader

# ============================================================
# SETTINGS
# ============================================================
DEBUG_MODE = True   # Set to False to reduce console debug output

# ============================================================
# FOLDERS
# ============================================================
input_folder = r"\\nu\GIS\Projects\2026_Projects\2026-Invoice-descriptions\rhondab-files\orig-Copy"
ocr_folder = r"\\nu\gis\Projects\2026_Projects\2026-Invoice-descriptions\rhondab-files\orig-copy-output"

os.makedirs(ocr_folder, exist_ok=True)

# Timestamped CSV log
run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_folder = os.path.join(ocr_folder, "logs")
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, f"rename_log_{run_timestamp}.csv")

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

GENERIC_IGNORE_TERMS = [
    "subtotal", "tax", "total", "balance", "invoice", "bill to", "ship to",
    "payment", "terms", "tracking", "order summary", "thank you", "account",
    "customer", "page", "amount due", "discount", "approved", "carrier",
    "branch", "customer id", "po number", "net due date", "disc due date",
    "unit price", "extended price", "pricing", "uom", "quantities",
    "lead law warning", "non-potable", "buyer is solely responsible",
    "not lead free", "anticipated for human consumption",
    "bedford regional water authority", "falling creek", "bedford",
    "invoice number", "S390563200102"
]

# ============================================================
# VENDOR PROFILES
# ============================================================
VENDOR_PROFILES = {
    "LMC": {
    "markers": [
        "2724 Nicholas Ave",
        "www.lmcsafety.com",
        "(800) 676-3427"
    ],
    
    "date_patterns": [
        r"Invoice Date[:\s]+(\d{1,2}/\d{1,2}/\d{4})",
        r"Invoice Date[:\s]+(\d{1,2}/\d{1,2}/\d{2})",
        r"Date[:\s]+(\d{1,2}/\d{1,2}/\d{4})",
        r"Date[:\s]+(\d{1,2}/\d{1,2}/\d{2})"

    ],
        "ignore_terms": [
            "subtotal",
            "total due",
            "terms",
            "page",
            "approved",
            "remit to",
            "invoice sub-total"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": "approved_code_note"
},
    
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
            r"Order Placed:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Order Date:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Order Placed:\s*(\d{1,2}/\d{1,2}/\d{2})",
            r"Order Date:\s*(\d{1,2}/\d{1,2}/\d{2})"
        ],
        "ignore_terms": [
            "return window",
            "ship to",
            "payment method",
            "order summary"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": "approved_code_note"
    },

    "TipcoTech": {
        "markers": [
            "tipcotech.com",
            "tipco",
            "owings mills",
            "cronhill"
        ],
        "date_patterns": [
            r"Invoice Date[:\s]+(\d{1,2}/\d{1,2}/\d{4})",
            r"Invoice\s*Date\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"Invoice Date[:\s]+(\d{1,2}/\d{1,2}/\d{2})",
            r"Invoice\s*Date\s+(\d{1,2}/\d{1,2}/\d{2})",
            r"Order Date[:\s]+(\d{1,2}/\d{1,2}/\d{4})",
            r"Order Date[:\s]+(\d{1,2}/\d{1,2}/\d{2})"
        ],
        "ignore_terms": [
            "approved", "please email", "carrier", "tracking #", "invoice date", "ship to",
            "bill to", "branch", "order number", "customer id", "customer fulfillment member",
            "pricing uom", "extended price", "unit price", "discount amount", "original",
            "net due date", "disc due date", "pick ticket no"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": "approved_code_note"
    },

    "Ferguson": {
        "markers": [
            "ferguson",
            "ferguson waterworks",
            "military highway",
            "chesapeake"
        ],
        "date_patterns": [
            r"INVOICE DATE[:\s]+(\d{1,2}/\d{1,2}/\d{2})",
            r"INVOICE DATE[:\s]+(\d{1,2}/\d{1,2}/\d{4})",
            r"Invoice Date[:\s]+(\d{1,2}/\d{1,2}/\d{2})",
            r"Invoice Date[:\s]+(\d{1,2}/\d{1,2}/\d{4})"
        ],
        "ignore_terms": [
            "job name", "bedford regional water authority", "falling creek", "bedford", "tax code",
            "customer order number", "item number", "lead law warning", "non-potable",
            "buyer is solely responsible", "not lead free", "anticipated for human consumption",
            "invoice sub-total", "approved", "remit to change", "please refer to invoice number",
            "master account number", "terms", "net 10th prox", "original invoice", "total due"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": "approved_code_note"
    },

    "IslandCreekDiesel": {
        "markers": [
            "island creek diesel",
            "angel place",
            "huddleston",
            "islandcreekdiesel@gmail.com"
        ],
        "date_patterns": [
            r"Date:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Date:\s*(\d{1,2}/\d{1,2}/\d{2})"
        ],
        "ignore_terms": [
            "subtotal", "amount", "rate", "invoice", "remit payment to", "bill to", "page:"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": "approved_code_note"
    },

    "glenwood_energy": {
        "markers": [
            "2074 smith mountain lake pkwy",
            "540-297-5297",
            "glenwood energy"
        ],
        "date_patterns": [
            r"Date:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Date:\s*(\d{1,2}/\d{1,2}/\d{2})"
        ],
        "ignore_terms": [
            "terms", "net 10", "subtotal", "amount", "rate", "invoice", "remit payment to",
            "bill to", "page:", "2074 smith mountain lake pkwy", "540-297-5297",
            "glenwood energy", "smith mountain lake pkwy"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": "approved_code_note"
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
            r"INVOICE DATE:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"INVOICE DATE:\s*(\d{1,2}/\d{1,2}/\d{2})",
            r"Order Date:\s*([A-Za-z]+ \d{1,2}, \d{4})",
            r"Order Date:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Order Date:\s*(\d{1,2}/\d{1,2}/\d{2})",
            r"Order Placed:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Order Placed:\s*(\d{1,2}/\d{1,2}/\d{2})"
        ],
        "ignore_terms": [
            "ot our truck", "bedford regional water authority", "falling creek", "bedford",
            "terms", "subtotal", "amount", "rate", "invoice", "ship date", "unit price",
            "writer", "ext price", "s39056", "invoice number", "remit to:", "invoice date",
            "salesperson", "customer number", "customer po number"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": ""
    },

    "Fortiline": {
        "markers": [
            "15850 dallas pkwy", "dallas, tx 75248", "po box 744053", "fortiline"
        ],
        "date_patterns": [
            r"INVOICE DATE:\s*([A-Za-z]+ \d{1,2}, \d{4})",
            r"INVOICE DATE:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"INVOICE DATE:\s*(\d{1,2}/\d{1,2}/\d{2})",
            r"Order Date:\s*([A-Za-z]+ \d{1,2}, \d{4})",
            r"Order Date:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Order Date:\s*(\d{1,2}/\d{1,2}/\d{2})",
            r"Order Placed:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Order Placed:\s*(\d{1,2}/\d{1,2}/\d{2})"
        ],
        "ignore_terms": [
            "lead time", "ot our truck", "invooice number", "bedford regional water authority",
            "falling creek", "bedford", "terms", "subtotal", "amount", "rate", "invoice",
            "ship date", "unit price", "writer", "ext price"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": "approved_code_note"
    },

    "BP_business": {
        "markers": [
            "po box 1239",
            "covington la 70434",
            "bp business solutions"
        ],
        "date_patterns": [
            r"INVOICE DATE:\s*([A-Za-z]+ \d{1,2}, \d{4})",
            r"INVOICE DATE:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"INVOICE DATE:\s*(\d{1,2}/\d{1,2}/\d{2})",
            r"Order Date:\s*([A-Za-z]+ \d{1,2}, \d{4})",
            r"Order Date:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Order Date:\s*(\d{1,2}/\d{1,2}/\d{2})",
            r"Order Placed:\s*(\d{1,2}/\d{1,2}/\d{4})",
            r"Order Placed:\s*(\d{1,2}/\d{1,2}/\d{2})"
        ],
        "ignore_terms": [
            "current activity summary",
            "summary of activity this reporting period",
            "invoice number",
            "bedford regional water authority",
            "falling creek",
            "bedford",
            "terms",
            "subtotal",
            "amount",
            "rate",
            "invoice",
            "ship date",
            "unit price",
            "writer",
            "ext price",
            "card activity details sorted by customer_id"
        ],
        "date_strategy": "pattern_list",
        "description_strategy": "fixed",
        "fixed_description": "vehicle-fuel-purchases"
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
            "description",
            "notes"
        ])

def write_log(stage, source_file="", ocr_file="", final_file="", status="", vendor="",
              date_part="", description="", notes=""):
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
            description,
            notes
        ])

# ============================================================
# HELPERS
# ============================================================
def clean_filename(text):
    """Keep only letters, numbers, dash, underscore."""
    return "".join(c for c in text if c.isalnum() or c in ("-", "_"))

def parse_date_string(raw):
    raw = raw.strip()
    date_formats = [
        "%B %d, %Y",
        "%m/%d/%Y",
        "%m/%d/%y",
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

def move_failed_input_file(input_path, original_filename, reason=""):
    """
    Move the original input PDF into the OCR output folder and prefix it with '_failed_'.
    If the target name already exists, append a counter.
    Returns the final moved filename, or an empty string if move failed.
    """
    failed_name = f"_failed_{original_filename}"
    failed_path = os.path.join(ocr_folder, failed_name)

    base, ext = os.path.splitext(failed_name)
    counter = 1
    while os.path.exists(failed_path):
        failed_name = f"{base}_{counter}{ext}"
        failed_path = os.path.join(ocr_folder, failed_name)
        counter += 1

    try:
        shutil.move(input_path, failed_path)
        print(f"Moved failed OCR file → {failed_name}")
        if reason:
            print(f"  Reason: {reason}")
        return failed_name
    except Exception as e:
        print(f"Could not move failed OCR file {original_filename}: {e}")
        return ""

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
    for label in GENERIC_DATE_LABELS:
        pattern1 = rf"{re.escape(label)}\s*([A-Za-z]+ \d{{1,2}}, \d{{4}})"
        m1 = re.search(pattern1, text, re.IGNORECASE)
        if m1:
            return parse_date_string(m1.group(1))

        pattern2 = rf"{re.escape(label)}\s*(\d{{1,2}}/\d{{1,2}}/\d{{4}})"
        m2 = re.search(pattern2, text, re.IGNORECASE)
        if m2:
            return parse_date_string(m2.group(1))

        pattern3 = rf"{re.escape(label)}\s*(\d{{1,2}}/\d{{1,2}}/\d{{2}})"
        m3 = re.search(pattern3, text, re.IGNORECASE)
        if m3:
            return parse_date_string(m3.group(1))

    generic_patterns = [
        r"([A-Za-z]+ \d{1,2}, \d{4})",
        r"(\d{1,2}/\d{1,2}/\d{4})",
        r"(\d{1,2}/\d{1,2}/\d{2})",
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

    return extract_date_generic(text, vendor_name)

DATE_STRATEGIES = {
    "generic": extract_date_generic,
    "pattern_list": extract_date_from_profile_patterns
}

def extract_date(text, vendor_name):
    profile = get_profile(vendor_name)
    strategy = profile.get("date_strategy", "generic")

    extractor = DATE_STRATEGIES.get(strategy, extract_date_generic)
    return extractor(text, vendor_name)

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

    header_index = None
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if sum(1 for keyword in header_keywords if keyword in line_lower) >= 2:
            header_index = i
            break

    if header_index is None:
        return extract_description_generic(text, vendor_name)

    candidate_lines = lines[header_index + 1: header_index + 20]

    def strip_trailing_price_tokens(line):
        tokens = line.split()

        while tokens:
            last = tokens[-1]
            if re.fullmatch(r"[\$]?\d[\d,]*\.?\d*", last) or re.fullmatch(r"\d+\.\d{2}", last):
                tokens.pop()
            else:
                break

        return " ".join(tokens)

    scored = []
    for idx, line in enumerate(candidate_lines):
        line_clean = strip_trailing_price_tokens(line)

        if not line_clean.strip():
            continue

        s = score_candidate_line(line_clean, ignore_terms)

        if idx < 6:
            s += 2

        if re.search(r"[A-Za-z]", line_clean) and re.search(r"\d", line_clean):
            s += 2

        if re.search(r"(lead law warning|non-potable|buyer is solely responsible|not lead free|human consumption)", line_clean, re.IGNORECASE):
            s -= 25

        if re.search(r"\b(total|subtotal|tax|amount due)\b", line_clean, re.IGNORECASE):
            s -= 10

        if s > 0:
            scored.append((s, idx, line_clean))

    if not scored:
        return extract_description_generic(text, vendor_name)

    scored.sort(reverse=True, key=lambda x: x[0])
    _, best_idx, best_line = scored[0]

    combined = best_line

    if best_idx + 1 < len(candidate_lines):
        next_line = candidate_lines[best_idx + 1].strip()

        if next_line:
            next_line_clean = strip_trailing_price_tokens(next_line)

            if (
                not contains_ignore_term(next_line_clean, ignore_terms)
                and not is_mostly_numeric_or_price(next_line_clean)
                and len(next_line_clean.split()) >= 2
                and not re.search(r"\b(total|subtotal|tax|amount due)\b", next_line_clean, re.IGNORECASE)
                and not re.search(r"(lead law warning|non-potable|buyer is solely responsible|not lead free|human consumption)", next_line_clean, re.IGNORECASE)
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

def extract_description_ferguson(text, vendor_name):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    ignore_terms = get_ignore_terms(vendor_name)

    header_index = None
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if "item number" in line_lower and "description" in line_lower:
            header_index = i
            break

    if header_index is None:
        return extract_description_table_basic(text, vendor_name)

    candidate_lines = lines[header_index + 1: header_index + 4]

    bad_patterns = [
        r"\bterms\b",
        r"\bnet\s+\d",
        r"\boriginal invoice\b",
        r"\btotal due\b",
        r"\binvoice sub-?total\b",
        r"\bapproved\b",
        r"\bremit to change\b",
        r"\blead law warning\b",
        r"\bnon-potable\b",
        r"\bbuyer is solely responsible\b"
    ]

    def is_bad_line(line):
        line_lower = line.lower()
        if contains_ignore_term(line, ignore_terms):
            return True
        return any(re.search(pattern, line_lower, re.IGNORECASE) for pattern in bad_patterns)

    def clean_item_description(desc):
        desc = desc.strip()
        desc = re.sub(r'\s+\d+(?:\.\d+)?\s+[A-Z]{1,3}\s+\d+(?:\.\d+)?\s*$', '', desc)
        desc = re.sub(r'\s+\d+(?:\.\d+)?\s*$', '', desc)
        desc = re.sub(r'\s+', ' ', desc).strip()
        return desc

    for line in candidate_lines:
        if is_bad_line(line):
            continue

        match = re.match(
            r'^\s*\d+\s+\d+\s+[A-Z0-9-]+\s+(.+?)\s+\d+(?:\.\d+)?\s+[A-Z]{1,3}\s+\d+(?:\.\d+)?\s*$',
            line
        )
        if match:
            desc = clean_item_description(match.group(1))
            if desc:
                return clean_description_tokens(desc, max_words=10)

    for line in candidate_lines:
        if is_bad_line(line):
            continue

        line2 = re.sub(r'^\s*\d+\s+\d+\s+[A-Z0-9-]+\s+', '', line)
        line2 = re.sub(r'\s+\d+(?:\.\d+)?\s+[A-Z]{1,3}\s+\d+(?:\.\d+)?\s*$', '', line2)

        if is_bad_line(line2):
            continue
        if is_mostly_numeric_or_price(line2):
            continue

        if re.search(r"[A-Za-z]", line2):
            desc = clean_item_description(line2)
            if desc:
                return clean_description_tokens(desc, max_words=10)

    return extract_description_table_basic(text, vendor_name)

def extract_description_approved_code_note(text, vendor_name):
    """
    Find APPROVED -> item code below it -> capture next 1-3 lines under that code.
    Falls back to Ferguson/table parsing if note block is missing.
    """
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    ignore_terms = get_ignore_terms(vendor_name)

    approved_index = None
    for i, line in enumerate(lines):
        if "approved" in line.lower():
            approved_index = i
            break

    if approved_index is None:
        if vendor_name == "Ferguson":
            return extract_description_ferguson(text, vendor_name)
        return extract_description_table_basic(text, vendor_name)

    code_index = None
    code_pattern = r'^[A-Z0-9]{3,8}-[A-Z0-9]{2,8}$'

    search_lines = lines[approved_index + 1: approved_index + 6]
    for offset, line in enumerate(search_lines, start=1):
        if re.fullmatch(code_pattern, line.strip()):
            code_index = approved_index + offset
            break

    if code_index is None:
        if vendor_name == "Ferguson":
            return extract_description_ferguson(text, vendor_name)
        return extract_description_table_basic(text, vendor_name)

    candidate_lines = lines[code_index + 1: code_index + 4]

    stop_patterns = [
        r"\bterms\b",
        r"\btotal due\b",
        r"\boriginal invoice\b",
        r"\bremit\b",
        r"\binvoice sub-?total\b",
        r"\bpayment\b",
        r"\bmaster account\b",
        r"\bpage\b",
        r"\binvoice number\b"
    ]

    def is_stop_line(line):
        line_lower = line.lower()
        if contains_ignore_term(line, ignore_terms):
            return True
        return any(re.search(pattern, line_lower, re.IGNORECASE) for pattern in stop_patterns)

    kept_lines = []
    for line in candidate_lines:
        if is_stop_line(line):
            break

        if is_mostly_numeric_or_price(line):
            continue

        if re.fullmatch(code_pattern, line.strip()):
            continue

        kept_lines.append(line)

    if not kept_lines:
        if vendor_name == "Ferguson":
            return extract_description_ferguson(text, vendor_name)
        return extract_description_table_basic(text, vendor_name)

    combined = " ".join(kept_lines)
    combined = re.sub(r"\s+", " ", combined).strip()

    return clean_description_tokens(combined, max_words=12)

def extract_description_fixed(text, vendor_name):
    profile = get_profile(vendor_name)
    return profile.get("fixed_description", "nophrase")

DESCRIPTION_STRATEGIES = {
    "generic": extract_description_generic,
    "amazon": extract_description_amazon,
    "table_basic": extract_description_table_basic,
    "ferguson": extract_description_ferguson,
    "approved_code_note": extract_description_approved_code_note,
    "fixed": extract_description_fixed,
}

def extract_description(text, vendor_name):
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
                failed_name = move_failed_input_file(
                    input_path=input_path,
                    original_filename=file,
                    reason="OCR returned non-zero exit code"
                )

                write_log(
                    stage="ocr",
                    source_file=file,
                    ocr_file=failed_name,
                    status="failed",
                    notes=result.stderr.strip() if result.stderr.strip() else "OCR failed"
                )
                continue

            if not os.path.exists(output_path):
                failed_name = move_failed_input_file(
                    input_path=input_path,
                    original_filename=file,
                    reason="OCR reported success, but output file not found"
                )

                write_log(
                    stage="ocr",
                    source_file=file,
                    ocr_file=failed_name,
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
            failed_name = move_failed_input_file(
                input_path=input_path,
                original_filename=file,
                reason=f"OCR exception: {e}"
            )

            write_log(
                stage="ocr",
                source_file=file,
                ocr_file=failed_name,
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
            print(f"No text found after OCR or from original PDF: {file}")
            write_log(
                stage="rename",
                ocr_file=file,
                status="skipped",
                notes="No text found after OCR/original PDF"
            )
            continue

        # Keep line breaks for line-based parsing; normalize spaces/tabs only
        text = re.sub(r"[ \t]+", " ", text)

        vendor_name = detect_vendor(text)
        safe_vendor = clean_filename(vendor_name) if vendor_name != "Unknown" else "Unknown"

        date_part = extract_date(text, vendor_name)
        description = extract_description(text, vendor_name)
        description = clean_filename(description)

        if DEBUG_MODE:
            print("DEBUG EXTRACTION:")
            print(f"  Vendor:      {vendor_name}")
            print(f"  Date:        {date_part}")
            print(f"  Description: {description}")
            print("-" * 40)

        base_name = f"{date_part}_{safe_vendor}_{description}"
        base_name = clean_filename(base_name)
        base_name = base_name[:140]

        if base_name in ("nodate_Unknown_nophrase", "nodate_Unknown_"):
            print(f"Skipping low-confidence file: {file}")
            write_log(
                stage="rename",
                ocr_file=file,
                status="skipped",
                vendor=vendor_name,
                date_part=date_part,
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