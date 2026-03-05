
from arcgis.gis import GIS
import csv
import os
import arcpy
import urllib3

# Environment settings
arcpy.env.overwriteOutput = True

# Suppress HTTPS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -----------------------------
# INPUT PARAMETERS
# -----------------------------
# Portal connection details
PORTAL_URL = "https://bedfordvagis.maps.arcgis.com"  # e.g., https://www.arcgis.com or Enterprise portal
USERNAME = "brwa.sync_bedfordvagis"
PASSWORD = "E&MBp^U@)4ybMWq"

# Hosted Feature Service Item ID to search for
FEATURE_SERVICE_ITEM_ID = "51bf387eb5a74afa84ef2b11d8424b95"  # Replace with your feature service item ID

# Output CSV file path
OUTPUT_CSV = r"C:\Work\maps_apps_report.csv"

# Item types to search
ITEM_TYPES = ["Web Map", "Web Mapping Application", "Dashboard", "StoryMap"]

# -----------------------------
# Connect to GIS
# -----------------------------
gis = GIS(PORTAL_URL, USERNAME, PASSWORD)
print("Connected to GIS successfully.")

# -----------------------------
# Search and collect matches
# -----------------------------
matching_items = []

for item_type in ITEM_TYPES:
    print(f"Searching for {item_type}s referencing Item ID: {FEATURE_SERVICE_ITEM_ID}")
    # Search for items that might reference the given Item ID
    items = gis.content.search(query="", item_type=item_type, max_items=-1)

    for item in items:
        try:
            data = item.get_data()
            if data and FEATURE_SERVICE_ITEM_ID in str(data):
                matching_items.append({
                    "Title": item.title,
                    "Type": item.type,
                    "Owner": item.owner,
                    "Item ID": item.id,
                    "URL": item.url,
                    "Last Modified": item.modified.strftime("%Y-%m-%d") if item.modified else "N/A",
                    "Sharing": item.shared_with if hasattr(item, "shared_with") else "N/A"
                })
        except Exception as e:
            print(f"Could not process {item_type} '{item.title}': {e}")

# -----------------------------
# Write results to CSV
# -----------------------------
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Title", "Type", "Owner", "Item ID", "URL", "Last Modified", "Sharing"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(matching_items)

print(f"Report generated successfully: {OUTPUT_CSV}")
print(f"Total matching items: {len(matching_items)}")