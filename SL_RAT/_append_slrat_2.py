# update the slrat_score and slrat_score_date fields in the target feature service based on the source feature class
# using spatial selection and proximity matching within 30m
# This script requires ArcPy and the ArcGIS API for Python to be installed and configured 
# with the appropriate credentials to access the source feature class and target feature service.
# The script assumes that the source feature class is a point feature class with fields "Assessment" and "MeasDate"
# and the target feature service has fields "slrat_score" and "slrat_score_date" that need to be updated.
# 


import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# Environment settings
arcpy.env.overwriteOutput = True

# parameters
source_fc = r"\\nu\gis\Projects\2025_Projects\202503_SL_RAT_Data\202503_SL_RAT_Data.gdb\Forest_to_point"  # Replace with your geodatabase path and feature class name
target_item_id = "51bf387eb5a74afa84ef2b11d8424b95"  # Replace with the Item ID of the hosted feature service in ArcGIS Online
infield1 = "AssessInt"  # Field name in source feature class
infield2 = "MeasDate"  # Field name in source feature class
outfield1 = "slrat_score"  # Field name in target feature service
outfield2 = "slrat_score_date"  # Field name in target feature service

""" arcpy.management.AddField(
    in_table="source_fc",
    field_name="AssessInt",
    field_type="SHORT",
    field_precision=None,
    field_scale=None,
    field_length=None,
    field_alias="",
    field_is_nullable="NULLABLE",
    field_is_required="NON_REQUIRED",
    field_domain=""
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateField(
    in_table="Source_fc",
    field="AssessInt",
    expression="!Assessment!",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.FeatureToPoint(
    in_features="source_fc",
    out_feature_class=r"\\nu\gis\Projects\2025_Projects\202503_SL_RAT_Data\202503_SL_RAT_Data.gdb\Forest_to_point",
    point_location="INSIDE"
) """


# ArcGIS Online credentials
username = 'j.hayes_bedfordvagis'
password = 'letrbuck4EO!'

# Connect to ArcGIS Online
gis = GIS("https://bedfordvagis.maps.arcgis.com", username=username, password=password)

# Retrieve the feature service item using the item ID
print(f"Fetching target layer using item ID: {target_item_id}")
target_item = gis.content.get(target_item_id)

# Ensure the item is valid and is a feature service
if target_item and target_item.type == "Feature Service":
    layers = target_item.layers
    if layers:
        target_layer_url = layers[0].url  # First layer in the service
        print(f"Target feature service found, using first layer: {target_layer_url}")
    else:
        print("No layers found in the feature service.")
        exit()
else:
    print("Invalid item ID or the item is not a feature service.")
    exit()

# Set environment settings
arcpy.env.overwriteOutput = True

# Create a layer from the source feature class
print("Creating source layer...")
arcpy.MakeFeatureLayer_management(source_fc, "source_lyr")
print("Source layer created.")

# Create a feature layer for the target hosted feature service
print("Creating target layer from hosted feature service...")
arcpy.management.MakeFeatureLayer(target_layer_url, "target_lyr")
print("Target layer created.")

# Perform spatial selection: Select target features within 30m of source
print("Performing spatial selection...")
arcpy.management.SelectLayerByLocation("target_lyr", "WITHIN_A_DISTANCE", "source_lyr", 10, "NEW_SELECTION")

# Check the number of selected target features
selected_count = int(arcpy.GetCount_management("target_lyr").getOutput(0))
print(f"Selected {selected_count} target features for update.")

if selected_count == 0:
    print("No features selected. Exiting script.")
    exit()

# Store source features in a LIST instead of a dictionary
source_data = []
with arcpy.da.SearchCursor("source_lyr", ["SHAPE@", infield1, infield2]) as source_cursor:
    for row in source_cursor:
        source_data.append((row[0], row[1], row[2]))  # (Geometry, Assessment, MeasDate)
print(f"Stored {len(source_data)} source features for matching.")

# Update target features based on spatial proximity
updated_count = 0
with arcpy.da.UpdateCursor("target_lyr", ["SHAPE@", outfield1, outfield2]) as target_cursor:
    for target_row in target_cursor:
        target_geom = target_row[0]  # Get geometry of target feature

        # Iterate through source features and find the closest match
        for source_geom, source_assessment, source_measdate in source_data:
            if target_geom.distanceTo(source_geom) <= 30:  # Check within 30m
                print(f"Updating target feature at {target_geom.centroid} with Assessment: {source_assessment}, MeasDate: {source_measdate}")
                target_row[1] = source_assessment
                target_row[2] = source_measdate
                target_cursor.updateRow(target_row)
                updated_count += 1
                break  # Stop after the first matching source is found

print(f"Successfully updated {updated_count} target features.")

# clean up
del source_cursor
del target_cursor

print("Field update completed successfully.")