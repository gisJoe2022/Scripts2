import arcpy
from arcgis.gis import GIS

# Environment settings
arcpy.env.overwriteOutput = True

# Login to ArcGIS Online
gis = GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Define source and target feature classes
source_fc = r"\\nu\gis\Projects\2025_Projects\202503_SL_RAT_Data\202503_SL_RAT_Data.gdb\Enhanced_Export_Bedford_Regional_Water_Authority__VA__30January2025"
source_fields = ["CGPSAssess", "MeasDate", "AssessText"]  # Add new source fields

target_fc = r"\\nu\gis\Projects\2025_Projects\202503_SL_RAT_Data\202503_SL_RAT_Data.gdb\Gravity_Main_Sewer_ExportFeatures"
target_fields = ["CGPSassess", "MeasDate", "AssessText"]  # Add corresponding target fields

# Create feature layers to allow spatial selection
arcpy.MakeFeatureLayer_management(source_fc, "source_layer")
arcpy.MakeFeatureLayer_management(target_fc, "target_layer")

# Add spatial index to the source for performance optimization
arcpy.management.AddSpatialIndex("source_layer")

# Process updates
try:
    with arcpy.da.SearchCursor("source_layer", ["SHAPE@"] + source_fields) as source_cursor:
        for source_row in source_cursor:
            source_geometry = source_row[0]
            source_values = source_row[1:]  # Extract field values

            # Select target features within 30 feet of the source geometry
            arcpy.management.SelectLayerByLocation(
                "target_layer", "HAVE_THEIR_CENTER_IN", source_geometry, "20 Feet", "NEW_SELECTION"
            )

            # Update selected features in the target feature class
            with arcpy.da.UpdateCursor("target_layer", target_fields) as target_cursor:
                for target_row in target_cursor:
                    target_row[:] = source_values  # Assign values from source
                    target_cursor.updateRow(target_row)

    print("Field values updated successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up layers
    arcpy.Delete_management("source_layer")
    arcpy.Delete_management("target_layer")




""" 
import arcpy
from arcgis.gis import GIS

# Environment settings
arcpy.env.overwriteOutput = True

# Login to ArcGIS Online
gis = GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Define source and target feature classes
source_fc = r"\\nu\gis\Projects\2025_Projects\202503_SL_RAT_Data\202503_SL_RAT_Data.gdb\Enhanced_Export_Bedford_Regional_Water_Authority_sum2024"
source_field = "CGPSAssess"

target_fc = r"\\nu\gis\Projects\2025_Projects\202503_SL_RAT_Data\202503_SL_RAT_Data.gdb\Gravity_Main_Sewer_ExportFeatures"
target_field = "CGPSassess"

# Create feature layers to allow spatial selection
arcpy.MakeFeatureLayer_management(source_fc, "source_layer")
arcpy.MakeFeatureLayer_management(target_fc, "target_layer")

# Add spatial index to the source for performance optimization
arcpy.management.AddSpatialIndex("source_layer")

# Process updates
try:
    with arcpy.da.SearchCursor("source_layer", ["SHAPE@", source_field]) as source_cursor:
        for source_row in source_cursor:
            source_geometry = source_row[0]
            source_value = source_row[1]

            # Select target features within 30 feet of the source geometry
            arcpy.management.SelectLayerByLocation(
                "target_layer", "HAVE_THEIR_CENTER_IN", source_geometry, "20 Feet", "NEW_SELECTION"
            )

            # Update selected features in the target feature class
            with arcpy.da.UpdateCursor("target_layer", [target_field]) as target_cursor:
                for target_row in target_cursor:
                    target_row[0] = source_value
                    target_cursor.updateRow(target_row)
    
    print("Field values updated successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up layers
    arcpy.Delete_management("source_layer")
    arcpy.Delete_management("target_layer") """


#--------------------------------------------------------------------------------------------


""" import arcpy
import pandas as pd
import datetime
import os
from arcgis.gis import GIS

# Login to ArcGIS Online
gis = GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Define the path to your hosted feature layer
feature_layer = gis.content.get("b962ffe1427043e29953dfe5e0d258bb").layers[0]  # Replace with your feature layer item ID

# Get the current date in yyyymmdd format
current_date = datetime.datetime.now().strftime("%Y%m%d")

# Extract the feature layer name (if it's a path, extract the name from the file name)
#layer_name = feature_layer.properties.name
#print(layer_name)

# Define the output path for the Excel file
output_folder = r"C:\\Work\\Data_qc\\"  # Replace with your desired folder path

# Create the dynamic output filename using the date and feature layer name
output_excel = f"{current_date}_null_count.xlsx"
output_file = os.path.join(output_folder, output_excel)

# Get the total number of features in the feature layer
total_features = int(arcpy.management.GetCount(feature_layer.url)[0])

# Create a list to hold the field names and null counts
field_null_counts = []

# Get the field names from the feature layer
fields = arcpy.ListFields(feature_layer.url)

# Iterate through each field to count the null values
for field in fields:
    field_name = field.name
    if field.type not in ['OID', 'Geometry']:  # Ignore OID and Geometry fields
        null_count = 0
        with arcpy.da.SearchCursor(feature_layer.url, field_name) as cursor:
            for row in cursor:
                if row[0] is None:  # Check if the value is null
                    null_count += 1

        # Calculate the percentage of null values
        perc_total = (null_count / total_features) * 100 if total_features > 0 else 0
        # Append the field name, null count, and percTotal to the list
        field_null_counts.append({'Field': field_name, 'Null Count': null_count, 'percTotal': perc_total})

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(field_null_counts)

# Write the DataFrame to an Excel file
df.to_excel(output_file, index=False, engine='openpyxl')

# Confirm the file has been saved
print(f"Null value counts have been written to: {output_file}") """
