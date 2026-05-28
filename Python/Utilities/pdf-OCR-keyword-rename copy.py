import os
import re
import sys
import csv
import shutil
import subprocess
from datetime import datetime
from pypdf import PdfReader

# -------------------------
# FOLDERS
# -------------------------
input_folder = r"\\nu\GIS\Scripts\pdf-rename-test\test"
ocr_folder = r"\\nu\GIS\Scripts\pdf-rename-test\test-ocr-output"
log_folder = r"\\nu\GIS\Scripts\pdf-rename-test\test-ocr-output\logs"

os.makedirs(ocr_folder, exist_ok=True)
os.makedirs(log_folder, exist_ok=True)

# -------------------------
# TIMESTAMPED LOG FILE
# -------------------------
run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_folder, f"rename_log_{run_timestamp}.csv")

# -------------------------
# CONFIG
# -------------------------
vendors = [
    "Amazon", "AMZN", "Amazon.com", "Amazon Services",
    "Home Depot", "Homedepot", "business prime", "businessprime",
    "Staples", "TIPCO", "Office Depot", "OfficeMax", "CMC Supply, inc."
    "Grainger", "FERGUSON", "Island Creek Diesel, LLC." "FORTLINE WATERWORKS",
    "JAMES RIVER EQUIPMENT", "JAMES RIVER", "MORRIS", "MORRIS SUPPLY", 
    "MORRIS MATERIALS", "MORRIS SAND & GRAVEL"
]

keywords_map = {
    "lumber": ["2x4", "plywood", "board"],
    "network": ["ethernet", "switch", "router"],
    "office": ["paper", "pens", "notebook"],
    "lighting": ["led", "light", "lamp"],
    "power": ["inverter", "battery", "generator", "sine"]
}

date_labels = [
    "Order Placed:", "Order Placed", "Order Date:", "Order Date",
    "Invoice Date:", "Invoice Date",  "INVOICE DATE", 
    "Date of Purchase:", "Date of Purchase", "Purchase Date:", "Date Purchased", "PURCHASE DATE", ""
    "Transaction Date:",
    "Submitted:"
]

# -------------------------
# COUNTERS
# -------------------------
ocr_success_count = 0
ocr_failed_count = 0
rename_success_count = 0
rename_skipped_count = 0
input_pdf_count = 0

# -------------------------
# HELPERS
# -------------------------
def clean_filename(s):
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
    # Try "3 of: item description"
    match = re.search(r'\d+\s+of:\s*(.+)', text, re.IGNORECASE)
    if match:
        line = match.group(1).split("\n")[0].strip()
        words = line.split()
        if words:
            return "-".join(words[:4]) # Take first 4 words after "of:" in Amazon-style invoices

    # Fallback: first line with at least 4 words
    for line in text.splitlines():
        words = line.strip().split()
        if len(words) >= 4:
            return "-".join(words[:4])

    return "nophrase"

def ensure_log_file(path):
    with open(path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "stage",
            "original_file",
            "ocr_file",
            "final_file",
            "status",
            "date",
            "vendor",
            "keywords",
            "phrase",
            "notes"
        ])

def write_log(
    stage,
    original_file="",
    ocr_file="",
    final_file="",
    status="",
    date_part="",
    vendor_found="",
    keyword_part="",
    phrase_part="",
    notes=""
):
    with open(log_file, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            stage,
            original_file,
            ocr_file,
            final_file,
            status,
            date_part,
            vendor_found,
            keyword_part,
            phrase_part,
            notes
        ])

# -------------------------
# MAIN
# -------------------------
try:
    ensure_log_file(log_file)

    print("Python executable:", sys.executable)
    print("ocrmypdf on PATH:", shutil.which("ocrmypdf"))
    print("tesseract on PATH:", shutil.which("tesseract"))
    print("gswin64c on PATH:", shutil.which("gswin64c"))
    print(f"Input folder exists: {os.path.isdir(input_folder)}")
    print(f"OCR folder exists:   {os.path.isdir(ocr_folder)}")
    print(f"CSV log file:        {log_file}")
    print("-" * 60)

    # -------------------------
    # STEP 1: OCR PDFs
    # -------------------------
    files = list(os.listdir(input_folder))
    pdf_files = [f for f in files if f.lower().endswith(".pdf")]
    input_pdf_count = len(pdf_files)

    print(f"Found {input_pdf_count} PDF file(s) in input folder.")

    for file in pdf_files:
        # Skip already-processed style names
        if file.startswith("nodate_") or re.match(r"\d{4}-\d{2}-\d{2}_", file):
            msg = "Skipped because filename appears already processed"
            print(f"Skipping already processed file: {file}")
            write_log(
                stage="ocr",
                original_file=file,
                status="skipped",
                notes=msg
            )
            continue

        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(ocr_folder, file)

        if not os.path.isfile(input_path):
            msg = f"Missing input file: {input_path}"
            print(msg)
            write_log(
                stage="ocr",
                original_file=file,
                status="error",
                notes=msg
            )
            ocr_failed_count += 1
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

            if result.stdout.strip():
                print("  STDOUT:")
                print(result.stdout)

            if result.stderr.strip():
                print("  STDERR:")
                print(result.stderr)

            if result.returncode != 0:
                msg = result.stderr.strip() if result.stderr.strip() else "OCR returned non-zero exit code"
                print(f"❌ OCR FAILED for {file}")
                write_log(
                    stage="ocr",
                    original_file=file,
                    ocr_file=os.path.basename(output_path),
                    status="failed",
                    notes=msg
                )
                ocr_failed_count += 1
                continue

            if not os.path.exists(output_path):
                msg = f"OCR reported success, but output file not found: {output_path}"
                print(f"❌ {msg}")
                write_log(
                    stage="ocr",
                    original_file=file,
                    ocr_file=os.path.basename(output_path),
                    status="failed",
                    notes=msg
                )
                ocr_failed_count += 1
                continue

            print(f"✅ OCR complete: {file}")
            write_log(
                stage="ocr",
                original_file=file,
                ocr_file=os.path.basename(output_path),
                status="success",
                notes="OCR completed successfully"
            )
            ocr_success_count += 1

        except Exception as e:
            msg = f"OCR exception: {e}"
            print(f"❌ {msg}")
            write_log(
                stage="ocr",
                original_file=file,
                ocr_file=os.path.basename(output_path),
                status="error",
                notes=msg
            )
            ocr_failed_count += 1
            continue

    # -------------------------
    # STEP 2: RENAME OCR FILES
    # -------------------------
    print("\nStarting rename step...")
    ocr_files = list(os.listdir(ocr_folder))
    ocr_pdf_files = [f for f in ocr_files if f.lower().endswith(".pdf")]

    print(f"Found {len(ocr_pdf_files)} PDF file(s) in OCR folder.")

    for file in ocr_pdf_files:
        path = os.path.join(ocr_folder, file)
        print(f"\nProcessing OCR file: {file}")

        try:
            reader = PdfReader(path)
        except Exception as e:
            msg = f"Unreadable PDF: {e}"
            print(f"Skipping unreadable PDF: {file} ({e})")
            write_log(
                stage="rename",
                ocr_file=file,
                status="error",
                notes=msg
            )
            rename_skipped_count += 1
            continue

        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        if not text.strip():
            msg = "No text found after OCR"
            print(f"No text found after OCR: {file}")
            write_log(
                stage="rename",
                ocr_file=file,
                status="skipped",
                notes=msg
            )
            rename_skipped_count += 1
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

        if base_name == "nodate_Unknown_misc_nophrase":
            msg = "Low-confidence result; rename skipped"
            print(f"Skipping low-confidence file: {file}")
            write_log(
                stage="rename",
                ocr_file=file,
                status="skipped",
                date_part=date_part,
                vendor_found=vendor_found,
                keyword_part=keyword_part,
                phrase_part=phrase_part,
                notes=msg
            )
            rename_skipped_count += 1
            continue

        new_name = base_name + ".pdf"
        new_path = os.path.join(ocr_folder, new_name)

        counter = 1
        while os.path.exists(new_path) and os.path.abspath(new_path) != os.path.abspath(path):
            new_name = f"{base_name}_{counter}.pdf"
            new_path = os.path.join(ocr_folder, new_name)
            counter += 1

        if os.path.abspath(new_path) != os.path.abspath(path):
            old_name = file
            os.rename(path, new_path)
            print(f"Renamed → {new_name}")
            write_log(
                stage="rename",
                ocr_file=old_name,
                final_file=new_name,
                status="renamed",
                date_part=date_part,
                vendor_found=vendor_found,
                keyword_part=keyword_part,
                phrase_part=phrase_part,
                notes="File renamed successfully"
            )
            rename_success_count += 1
        else:
            print(f"Already correctly named: {file}")
            write_log(
                stage="rename",
                ocr_file=file,
                final_file=file,
                status="unchanged",
                date_part=date_part,
                vendor_found=vendor_found,
                keyword_part=keyword_part,
                phrase_part=phrase_part,
                notes="Filename already matched desired output"
            )
            rename_skipped_count += 1

    # -------------------------
    # SUMMARY
    # -------------------------
    print("\n" + "=" * 60)
    print("PROCESS COMPLETE")
    print("=" * 60)
    print(f"Input PDFs found:      {input_pdf_count}")
    print(f"OCR succeeded:         {ocr_success_count}")
    print(f"OCR failed/errors:     {ocr_failed_count}")
    print(f"Renamed successfully:  {rename_success_count}")
    print(f"Rename skipped/errors: {rename_skipped_count}")
    print(f"Log written to:        {log_file}")

except Exception as e:
    print("\nFATAL ERROR:")
    print(e)
    try:
        write_log(
            stage="fatal",
            status="error",
            notes=f"Fatal script error: {e}"
        )
    except Exception:
        pass
