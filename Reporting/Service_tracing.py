

import arcpy
from arcgis.gis import GIS
import csv
import os
import urllib3

# Environment settings
arcpy.env.overwriteOutput = True

# Suppress HTTPS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -----------------------------
# User Inputs
# -----------------------------
portal_url = "https://bedfordvagis.maps.arcgis.com"  # or your Enterprise portal URL
username = "brwa.sync_bedfordvagis"
password = "E&MBp^U@)4ybMWq"
item_id = "2d8fbc23152441b7b4d1a3695eb19ecf" # Feature service item ID to trace
output_csv = r"C:\Work\hydrants_maps_apps_report.csv" # Update to your desired output path

# -----------------------------
# Connect to GIS
# -----------------------------
print(f"DEBUG: portal_url={portal_url}")
print(f"DEBUG: username={username}")
print("DEBUG: attempting to connect to GIS...")
gis = GIS(portal_url, username, password)
print("DEBUG: connected to GIS")

# -----------------------------
# Search for maps and apps referencing the item
# -----------------------------
print(f"Searching for maps and apps referencing item ID: {item_id}")
search_query = f"{item_id} AND ('Web maps')"
print(f"DEBUG: search_query={search_query}")
items = gis.content.search(query=search_query, max_items=1000)
print(f"DEBUG: search returned {len(items)} items")

# -----------------------------
# Prepare CSV
# -----------------------------
fields = ["Title", "Type", "Owner", "Item ID", "URL"]
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)

    for item in items:
        print(f"DEBUG: writing item - id={item.id}, title={item.title}, type={item.type}")
        writer.writerow([item.title, item.type, item.owner, item.id, item.url])




