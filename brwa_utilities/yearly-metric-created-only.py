


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
    # FeatureServer root URLs, layer URLs, or item IDs all work
        "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Water_Meter_2021/FeatureServer"

]

# ---------------------------------
# OUTPUT FILE NAME
# ---------------------------------

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"water_report_{QUERY_YEAR}_{timestamp}.xlsx"
output_path = os.path.join(OUTPUT_FOLDER, output_filename)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------------------------
# TIME RANGE (UTC, Epoch Milliseconds)
# ---------------------------------

start_year = int(datetime(QUERY_YEAR, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
end_year = int(datetime(QUERY_YEAR + 1, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)

# ---------------------------------
# LOGIN
# ---------------------------------

gis = GIS("https://www.arcgis.com", USERNAME, PASSWORD)

# ---------------------------------
# SAFE LAYER RESOLUTION
# ---------------------------------

def get_layers(service_ref, gis):
    if isinstance(service_ref, str) and (
        "item.html" in service_ref or len(service_ref) == 32
    ):
        item = gis.content.get(service_ref)
        return item.layers if item else []

    if service_ref.lower().endswith("featureserver"):
        flc = FeatureLayerCollection(service_ref, gis)
        return flc.layers

    if "/featureserver/" in service_ref.lower():
        return [FeatureLayer(service_ref, gis)]

    raise ValueError(f"Unrecognized service reference: {service_ref}")

# ---------------------------------
# CREATED DATE FIELD DETECTION
# ---------------------------------

def get_creation_date_field(layer):
    editing_info = layer.properties.get("editingInfo")
    if not editing_info:
        return None
    return editing_info.get("creationDateField")

# ---------------------------------
# PROCESS SERVICES
# ---------------------------------

rows = []

for service_ref in FEATURE_SERVICES:
    print(f"\nProcessing: {service_ref}")

    try:
        layers = get_layers(service_ref, gis)
    except Exception as e:
        print(f"  ❌ Cannot resolve service: {e}")
        continue

    for layer in layers:
        layer_name = layer.properties.name

        if "query" not in layer.properties.capabilities.lower():
            print(f"  ⚠️ Skipping '{layer_name}' (query not supported)")
            continue

        created_field = get_creation_date_field(layer)

        if not created_field:
            print(f"  ⚠️ Skipping '{layer_name}' (no creation date tracking)")
            continue

        where = (
            f"{created_field} >= {start_year} "
            f"AND {created_field} < {end_year}"
        )

        try:
            count = layer.query(
                where=where,
                return_count_only=True
            )
        except Exception as e:
            print(f"  ❌ Query failed on '{layer_name}': {e}")
            print(f"     WHERE: {where}")
            continue

        rows.append({
            "Service Reference": service_ref,
            "Layer Name": layer_name,
            "Features Created": count
        })

        print(f"  ✅ {layer_name}: {count}")

# ---------------------------------
# WRITE TO EXCEL
# ---------------------------------

df = pd.DataFrame(
    rows,
    columns=[
        "Service Reference",
        "Layer Name",
        "Features Created"
    ]
)

total = df["Features Created"].sum() if not df.empty else 0
df.loc[len(df)] = ["ALL SERVICES", "ALL LAYERS", total]

df.to_excel(
    output_path,
    index=False,
    engine="openpyxl"
)

print("\n===================================")
print("✅ CREATED‑FEATURE REPORT COMPLETE")
print(f"File: {output_path}")
print(f"TOTAL features created in {QUERY_YEAR}: {total}")
print("===================================")