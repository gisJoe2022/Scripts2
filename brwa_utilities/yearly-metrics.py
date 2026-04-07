

from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection, FeatureLayer
from datetime import datetime, timezone
import pandas as pd
import os

# ---------------------------------
# CONFIGURATION
# ---------------------------------

USERNAME = "brwa.sync_bedfordvagis"
PASSWORD = "E&MBp^U@)4ybMWq"
OUTPUT_FOLDER = r"C:\GIS\Reports\Water"
QUERY_YEAR = 2025

FEATURE_SERVICES = [
    # Examples (any of these formats work):
    # "https://services.arcgis.com/XXXX/ArcGIS/rest/services/MyService/FeatureServer",
    # "https://services.arcgis.com/XXXX/ArcGIS/rest/services/MyService/FeatureServer/0",
    # "abcdef1234567890abcdef1234567890",
    # "https://www.arcgis.com/home/item.html?id=abcdef1234567890abcdef1234567890"
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Waterline_BRWA_Version2021/FeatureServer",
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Gravity_Main_Sewer_2020/FeatureServer"
]



# ---------------------------------
# BUILD OUTPUT FILE NAME
# ---------------------------------

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"water_report_{QUERY_YEAR}_{timestamp}.xlsx"
output_path = os.path.join(OUTPUT_FOLDER, output_filename)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------------------------
# TIME RANGE (UTC epoch milliseconds)
# ---------------------------------

start_year = int(datetime(QUERY_YEAR, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
end_year = int(datetime(QUERY_YEAR + 1, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)

# ---------------------------------
# LOGIN
# ---------------------------------

gis = GIS("https://bedfordvagis.maps.arcgis.com", USERNAME, PASSWORD)

# ---------------------------------
# SAFE LAYER RESOLUTION
# ---------------------------------

def get_layers(service_ref, gis):
    """Return a list of FeatureLayer objects from any valid AGOL reference."""

    # Item ID or item.html URL
    if isinstance(service_ref, str) and (
        "item.html" in service_ref or len(service_ref) == 32
    ):
        item = gis.content.get(service_ref)
        if not item:
            raise ValueError(f"Cannot resolve item: {service_ref}")
        return item.layers or []

    # FeatureServer root
    if service_ref.lower().endswith("featureserver"):
        flc = FeatureLayerCollection(service_ref, gis)
        return flc.layers

    # Individual layer
    if "/featureserver/" in service_ref.lower():
        return [FeatureLayer(service_ref, gis)]

    raise ValueError(f"Unrecognized service reference: {service_ref}")

# ---------------------------------
# EDITOR TRACKING FIELD DETECTION
# ---------------------------------

def get_editor_tracking_fields(layer):
    """Return actual editor tracking field names from layer metadata."""
    editing_info = layer.properties.get("editingInfo")
    if not editing_info:
        return None, None

    return (
        editing_info.get("creationDateField"),
        editing_info.get("editDateField")
    )

# ---------------------------------
# PROCESS SERVICES
# ---------------------------------

rows = [{}]

for service_ref in FEATURE_SERVICES:
    print(f"\nProcessing: {service_ref}")

    try:
        layers = get_layers(service_ref, gis)
    except Exception as e:
        print(f"  ❌ Unable to resolve service: {e}")
        continue

print("\n--- DEBUG: Reaching Excel write section ---")
print(f"Rows collected: {len(rows)}")
print(f"Output path:\n{output_path}")

df = pd.DataFrame(
    rows,
    columns=[
        "Service Reference",
        "Layer Name",
        "Features Created or Updated"
    ]
)

total = df["Features Created or Updated"].sum() if not df.empty else 0

df.loc[len(df)] = ["ALL SERVICES", "ALL LAYERS", total]

df.to_excel(
    output_path,
    index=False,
    engine="openpyxl"
)

print("✅ Excel file written successfully")
print("--- DEBUG: Script completed ---")

try:
    df.to_excel(
        output_path,
        index=False,
        engine="openpyxl"
    )
    print("✅ Excel write succeeded")
except Exception as e:
    print("❌ Excel write FAILED")
    raise

print("--- DEBUG: Script completed normally ---")
