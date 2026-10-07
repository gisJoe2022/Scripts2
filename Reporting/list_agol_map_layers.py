

from arcgis.gis import GIS
import pandas as pd
from datetime import datetime
import re

# ArcGIS Online credentials
username = "brwa.sync_bedfordvagis"
password = "E&MBp^U@)4ybMWq"

# Web Map Item ID
item_id = "a25774a725dc4355b3e84aa70bc0e561"

# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com", username, password)

# Get Web Map
wm = gis.content.get(item_id)

if not wm:
    raise Exception(f"Item not found: {item_id}")

print(f"Item Title: {wm.title}")
print(f"Item Type: {wm.type}")

if wm.type != "Web Map":
    raise Exception(f"Item is a '{wm.type}', not a Web Map.")

# Get Web Map JSON
data = wm.get_data()

rows = []


def process_layer(layer, group_name=None):
    """
    Processes layers recursively.
    Skips group layers but includes all layers inside them.
    """

    # Group layer
    if "layers" in layer and layer["layers"]:
        current_group = layer.get("title")

        for child in layer["layers"]:
            process_layer(child, current_group)

        return

    # Regular layer
    rows.append({
        "Category": "Operational Layer",
        "Group": group_name,
        "Name": layer.get("title"),
        "Item ID": layer.get("itemId"),
        "Layer ID": layer.get("id"),
        "URL": layer.get("url"),
        "Layer Type": layer.get("layerType"),
        "Visible": layer.get("visibility")
    })


# Process operational layers
for lyr in data.get("operationalLayers", []):
    process_layer(lyr)


# Process tables
for tbl in data.get("tables", []):
    rows.append({
        "Category": "Table",
        "Group": "",
        "Name": tbl.get("title"),
        "Item ID": tbl.get("itemId"),
        "Layer ID": tbl.get("id"),
        "URL": tbl.get("url"),
        "Layer Type": "Table",
        "Visible": ""
    })


# Process basemap layers
for lyr in data.get("baseMap", {}).get("baseMapLayers", []):
    rows.append({
        "Category": "Basemap Layer",
        "Group": "",
        "Name": lyr.get("title"),
        "Item ID": lyr.get("itemId"),
        "Layer ID": lyr.get("id"),
        "URL": lyr.get("url"),
        "Layer Type": lyr.get("layerType"),
        "Visible": ""
    })


# Create DataFrame
df = pd.DataFrame(rows)

# Sort output
df = df.sort_values(
    by=["Category", "Group", "Name"],
    na_position="last"
)

# Create safe filename from Web Map title
safe_title = re.sub(r'[<>:"/\\|?*]', '_', wm.title)

# Timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Output CSV path
output_csv = (
    rf"\\192.168.20.14\gis\Scripts\layer_list\{safe_title}_{timestamp}.csv"
)

# Export CSV
df.to_csv(output_csv, index=False)

print(f"Operational Layers: {len(data.get('operationalLayers', []))}")
print(f"Tables: {len(data.get('tables', []))}")
print(f"Rows Exported: {len(df)}")
print(f"Output CSV: {output_csv}")