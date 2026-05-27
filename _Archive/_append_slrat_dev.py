

# Import
import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import os
from datetime import datetime

# Environment settings
arcpy.env.overwriteOutput = True

# parameters

# source_fc = r"\\\\nu\\gis\\Projects\\2025_Projects\\202503_SL_RAT_Data\\SL_RAT_Data_2.gdb\\slratcurrent"  # Replace with your geodatabase path and feature class name
source_fc = r"S:\\Projects\\2025_Projects\\202503_SL_RAT_Data\\SL_RAT_Data_2.gdb\\slratcurrent"  # Replace with your geodatabase path and feature class name
target_item_id = "51bf387eb5a74afa84ef2b11d8424b95"  # Replace with the Item ID of the hosted feature service in ArcGIS Online
infield1 = "Assessment"  # Field name in source feature class
infield2 = "MeasDate"  # Field name in source feature class
outfield1 = "slrat_score"  # Field name in target feature service
outfield2 = "slrat_score_date"  # Field name in target feature service

# ArcGIS Online credentials
username = "brwa.sync_bedfordvagis" # Replace with your ArcGIS Online username
password = "E&MBp^U@)4ybMWq" # Replace with your ArcGIS Online password

# Convert source feature class to point feature class
#output_directory = r"\\\\nu\\gis\\Projects\\2025_Projects\\202503_SL_RAT_Data\\SL_RAT_Data_2.gdb"
output_directory = r"S:\\Projects\\2025_Projects\\202503_SL_RAT_Data\\SL_RAT_Data_2.gdb"
date_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
output_point_fc = os.path.join(output_directory, f"sl_rat_point_{date_time_str}")
arcpy.management.FeatureToPoint(source_fc, output_point_fc, "INSIDE")
# Update source_fc to use the new point feature class
source_fc = output_point_fc


# Add Assessment field to source_fc if it doesn't exist
fields = [f.name for f in arcpy.ListFields(source_fc)]
if "Assessment" not in fields:
    print("Adding field 'Assessment' to source feature class...")
    arcpy.AddField_management(source_fc, "Assessment", "LONG")
    print("Field 'Assessment' added.")
else:
    print("Field 'Assessment' already exists in source feature class.")

    # Calculate Assessment field from Assessment field in source_fc
    if "Assessment" in fields:
        print("Calculating 'Assessment' from 'Assessment' field...")
        arcpy.CalculateField_management(
            source_fc,
            field="Assessment",
            expression="!Assessment!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS"
        )
        print("'Assessment' field calculated.")
    else:
        print("Field 'Assessment' does not exist in source feature class.")


# Connect to ArcGIS Online
gis = GIS("https://bedfordvagis.maps.arcgis.com", username, password)

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
arcpy.management.SelectLayerByLocation("target_lyr", "WITHIN_A_DISTANCE", "source_lyr", "10 Feet", "NEW_SELECTION")

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

""" # clean up
del source_cursor
del target_cursor """

print("Field update completed successfully.")