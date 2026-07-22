

from pathlib import Path

# Change this to your folder path
folder = Path(r"\\nu\GIS\Scripts\pdf-rename-test\test")

# Get all PDF files in the folder, sorted by name
pdf_files = sorted(folder.glob("*.pdf"))

# First pass: rename to temporary names
temp_files = []
for i, pdf_file in enumerate(pdf_files, start=1):
    temp_name = folder / f"temp_rename_{i}.pdf"
    pdf_file.rename(temp_name)
    temp_files.append(temp_name)

# Second pass: rename temp files to final numeric names
for i, temp_file in enumerate(temp_files, start=1):
    final_name = folder / f"{i}.pdf"
    temp_file.rename(final_name)
    print(f'Renamed "{temp_file.name}" -> "{final_name.name}"')

print("Done.")
