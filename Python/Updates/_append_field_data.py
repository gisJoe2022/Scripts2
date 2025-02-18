

import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# enironment/workspace settings
arcpy.env.overwriteOutput = True

# Login to ArcGIS Online
gis =  GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Define the paths to your feature classes
#target_feature_service_url = "https://services.arcgis.com/your_org_id/arcgis/rest/services/your_feature_service/FeatureServer/0"

# Define the path to your hosted feature layer
#feature_layer = gis.content.get("b962ffe1427043e29953dfe5e0d258bb").layers[0]  # Replace with your feature layer item ID

source_fc = r"\\nu\gis\Projects\2025_Projects\202503_SL_RAT_Data\202503_SL_RAT_Data.gdb\Enhanced_Export_Bedford_Regional_Water_Authority_sum2024"
source_field = "CGPSAssess"

# Define the fields to update and the fields to get values from
target_fc = r"\\nu\gis\Projects\2025_Projects\202503_SL_RAT_Data\202503_SL_RAT_Data.gdb\Gravity_Main_Sewer_ExportFeatures"
#target_fcname = r"Gravity_Main_Sewer_ExportFeatures"
target_field = "CGPSassess"

# Access the hosted feature layer
target_fc = FeatureLayer(source_fc)

# Create a spatial index on the source feature class to improve performance
arcpy.management.AddSpatialIndex(source_fc)

# Use an Update Cursor to iterate through the target feature class and update the field based on proximity to the source feature class
with arcpy.da.UpdateCursor(source_fc, ["SHAPE@", source_field]) as source_cursor:
    for source_row in source_cursor:
        source_geometry = source_row[0]
        source_value = source_row[1]

        # Perform a spatial query to find the nearest feature in the target feature service
        spatial_query = arcpy.management.SelectLayerByLocation(
            target_fc, "HAVE_THEIR_CENTER_IN", source_geometry, search_distance="30"
        )

        # Use a Search Cursor to get the value from the source feature class
        with arcpy.da.UpdateCursor(spatial_query, ["SHAPE@", target_field]) as target_cursor:
            for target_row in target_cursor:
                target_row[1] = source_value
                target_cursor.updateRow(target_row)
                break  # Exit after the first match

print("Field values updated based on proximity.")