

from arcgis.gis import GIS
import csv
import os
import json
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

# Search mode: choose "item_id" or "url"
SEARCH_MODE = "item_id"  # options: "item_id" or "url"

# Hosted Feature Service Item ID (used if SEARCH_MODE = "item_id")
FEATURE_SERVICE_ITEM_ID = "51bf387eb5a74afa84ef2b11d8424b95"

# Feature Service URL (used if SEARCH_MODE = "url")
FEATURE_SERVICE_URL = "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Gravity_Main_Sewer_2020/FeatureServer"

# Output CSV file path
OUTPUT_CSV = r"C:\Work\reports\maps_apps_report.csv"

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
    print(f"Searching {item_type}s...")
    items = gis.content.search(query="", item_type=item_type, max_items=-1)

    for item in items:
        try:
            data = item.get_data() or {}

            # build token set depending on mode
            tokens = set()
            if SEARCH_MODE == "item_id":
                tokens.add(FEATURE_SERVICE_ITEM_ID)
            elif SEARCH_MODE == "url":
                tokens.add(FEATURE_SERVICE_URL)
                # also add base REST path without trailing layer index
                try:
                    parsed = FEATURE_SERVICE_URL.rstrip("/")
                    # remove trailing layer/index if present
                    if parsed.endswith("/FeatureServer") or parsed.endswith("/MapServer"):
                        tokens.add(parsed)
                    else:
                        # strip last numeric segment
                        parts = parsed.split("/")
                        if parts[-1].isdigit():
                            tokens.add("/".join(parts[:-1]))
                except Exception:
                    pass

            found_match = False
            match_field = ""

            # 1) quick JSON text search
            try:
                data_text = json.dumps(data)
            except Exception:
                data_text = str(data)

            for tok in tokens:
                if tok and tok in data_text:
                    found_match = True
                    match_field = f"json_contains:{tok}"
                    break

            # 2) operationalLayers detailed check (preferred for Web Maps)
            if not found_match and isinstance(data, dict) and "operationalLayers" in data:
                for layer in data.get("operationalLayers", []) or []:
                    # possible keys that reference services
                    for key in ("url", "itemId", "serviceItemId", "serviceUrl", "layerId", "id", "resource"):
                        try:
                            val = None
                            if isinstance(layer, dict):
                                val = layer.get(key)
                            else:
                                val = getattr(layer, key, None)
                            if val:
                                for tok in tokens:
                                    if tok and tok in str(val):
                                        found_match = True
                                        match_field = f"operationalLayers.{key}:{tok}"
                                        break
                                if found_match:
                                    break
                        except Exception:
                            continue
                    if found_match:
                        break

            # 3) layer objects attached to item (item.layers) may reference URLs
            if not found_match:
                try:
                    for lyr in getattr(item, "layers", []) or []:
                        lyr_url = getattr(lyr, "url", None)
                        lyr_id = getattr(lyr, "properties", None) or {}
                        for tok in tokens:
                            if tok and ((lyr_url and tok in lyr_url) or (isinstance(lyr_id, dict) and tok in json.dumps(lyr_id))):
                                found_match = True
                                match_field = f"item.layers:{tok}"
                                break
                        if found_match:
                            break
                except Exception:
                    pass

            if found_match:
                matching_items.append({
                    "Title": item.title,
                    "Type": item.type,
                    "Owner": item.owner,
                    "Item ID": item.id,
                    "URL": item.url,
                    #"Match Field": match_field,
                })
        except Exception as e:
            print(f"Could not process {item_type} '{item.title}': {e}")

# -----------------------------
# Write results to CSV
# -----------------------------
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Title", "Type", "Owner", "Item ID", "URL"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(matching_items)

print(f"Report generated successfully: {OUTPUT_CSV}")
print(f"Total matching items: {len(matching_items)}")