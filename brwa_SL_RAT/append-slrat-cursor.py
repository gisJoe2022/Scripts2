
# Script: append-slrat-cursor.py
# Description: Update hosted gravity main sewer on proximity to slrat point features using arcpy cursors.
# Note: This script is designed for ArcGIS Pro and requires appropriate permissions to access the hosted feature service.
# Author: Joe Hayes
# Date: 2026-04-16


import arcpy
import os
from datetime import datetime

# --------------------------------------------------
# ENVIRONMENT
# --------------------------------------------------
arcpy.env.overwriteOutput = True

# --------------------------------------------------
# PARAMETERS
# --------------------------------------------------

# Source points (local GDB)
source_fc = r"\\192.168.20.14\\gis\\Projects\\2025_Projects\\202503_SL_RAT_Data\\SL_RAT_Data.gdb\\c20206May1_FeatureToPoint"

# Target hosted feature layer (FeatureServer URL)
target_fc = (
    "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Gravity_Main_Sewer_2020/FeatureServer/0"
)

# Field mapping (POINT → LINE)
src_field_1 = "Assessment"
src_field_2 = "MeasDate"
tgt_field_1 = "slrat_score"
tgt_field_2 = "slrat_score_date"

# Search distance (units = projected units)
SEARCH_DISTANCE = 20 

# ArcGIS Online credentials
username = "brwa.sync_bedfordvagis"
password = "E&MBp^U@)4ybMWq"  # secure for production use

# Log output directory
output_dir = r"\\192.168.20.14\gis\Projects\2025_Projects\202503_SL_RAT_Data\logs"
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(output_dir, f"slrat_update_log_{timestamp}.txt")

# --------------------------------------------------
# LOGGING FUNCTION
# --------------------------------------------------
def log(message):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{time_str}] {message}"
    print(msg)
    with open(log_file, "a") as f:
        f.write(msg + "\n")

# --------------------------------------------------
# SIGN IN TO AGOL
# --------------------------------------------------
log("Signing in to ArcGIS Online...")
arcpy.SignInToPortal("https://www.arcgis.com", username, password)

# --------------------------------------------------
# METADATA / VALIDATION
# --------------------------------------------------
source_oid_field = arcpy.Describe(source_fc).OIDFieldName
log(f"Source OID field: {source_oid_field}")

source_fields = [f.name for f in arcpy.ListFields(source_fc)]
if src_field_1 not in source_fields or src_field_2 not in source_fields:
    raise RuntimeError("Required source fields are missing.")

# --------------------------------------------------
# LOAD SOURCE POINTS
# --------------------------------------------------
log("Loading source point features...")

source_data = []
all_source_oids = set()

with arcpy.da.SearchCursor(
    source_fc,
    ["SHAPE@", source_oid_field, src_field_1, src_field_2]
) as scur:
    for geom, oid, val1, val2 in scur:
        if geom:
            source_data.append((geom, oid, val1, val2))
            all_source_oids.add(oid)

log(f"Loaded {len(source_data)} source points.")

if not source_data:
    raise RuntimeError("No valid source points found.")

used_source_oids = set()

# --------------------------------------------------
# UPDATE TARGET LINE FEATURES
# --------------------------------------------------
log("Updating hosted line features...")
updated_count = 0

with arcpy.da.UpdateCursor(
    target_fc,
    ["SHAPE@", tgt_field_1, tgt_field_2]
) as ucur:

    for line_geom, _, _ in ucur:
        if not line_geom:
            continue

        min_dist = None
        matched_oid = None
        matched_val1 = None
        matched_val2 = None

        for pt_geom, pt_oid, src_val1, src_val2 in source_data:
            dist = line_geom.distanceTo(pt_geom)

            if dist <= SEARCH_DISTANCE and (min_dist is None or dist < min_dist):
                min_dist = dist
                matched_oid = pt_oid
                matched_val1 = src_val1
                matched_val2 = src_val2

        if matched_oid is not None:
            ucur.updateRow((line_geom, matched_val1, matched_val2))
            used_source_oids.add(matched_oid)
            updated_count += 1

log(f"Updated {updated_count} line features.")

# --------------------------------------------------
# REPORT UNUSED SOURCE POINTS (LOG ONLY)
# --------------------------------------------------
unused_source_oids = sorted(all_source_oids - used_source_oids)
unused_count = len(unused_source_oids)

log(f"{unused_count} source point(s) did NOT transfer values.")

if unused_source_oids:
    log("Unused source point OIDs:")
    log(", ".join(map(str, unused_source_oids)))
else:
    log("All source points were used at least once.")

# --------------------------------------------------
# COMPLETE
# --------------------------------------------------
log("Process completed successfully.")