""" import arcpy
import pandas as pd

# Define the path to your hosted feature layer
feature_layer = "https://webgis.bedfordcountyva.gov/arcgis/rest/services/OpenData/OpenDataBRWA/MapServer/2"  # Replace with your feature layer URL or path

# Define the output path for the Excel file
output_folder = r"C:\Work\Data_qc"  # Replace with your desired folder path
output_excel = "null_values_count.xlsx"
output_file = f"{output_folder}\\{output_excel}"

# Create a list to hold the field names and null counts
field_null_counts = []

# Get the field names from the feature layer
fields = arcpy.ListFields(feature_layer)

# Iterate through each field to count the null values
for field in fields:
    field_name = field.name
    if field.type not in ['OID', 'Geometry']:  # Ignore OID and Geometry fields
        null_count = 0
        with arcpy.da.SearchCursor(feature_layer, field_name) as cursor:
            for row in cursor:
                if row[0] is None:  # Check if the value is null
                    null_count += 1
        # Append the field name and null count to the list
        field_null_counts.append({'Field': field_name, 'Null Count': null_count})

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(field_null_counts)

# Write the DataFrame to an Excel file
df.to_excel(output_file, index=False, engine='openpyxl')

# Confirm the file has been saved
print(f"Null value counts have been written to: {output_file}")


import arcpy
import pandas as pd
import datetime

# Define the path to your hosted feature layer
feature_layer = "your_feature_layer_url_or_path"  # Replace with your feature layer URL or path

# Get the current date in yyyymmdd format
current_date = datetime.datetime.now().strftime("%Y%m%d")

# Extract the feature layer name (if it's a path, extract the name from the file name)
layer_name = feature_layer.split("\\")[-1].split(".")[0]  # This works for file paths, adjust for URLs if needed

# Define the output path for the Excel file
output_folder = r"C:\path\to\your\folder"  # Replace with your desired folder path

# Create the dynamic output filename using the date and feature layer name
output_excel = f"{current_date}_{layer_name}_null_values_count.xlsx"
output_file = f"{output_folder}\\{output_excel}"

# Create a list to hold the field names and null counts
field_null_counts = []

# Get the field names from the feature layer
fields = arcpy.ListFields(feature_layer)

# Iterate through each field to count the null values
for field in fields:
    field_name = field.name
    if field.type not in ['OID', 'Geometry']:  # Ignore OID and Geometry fields
        null_count = 0
        with arcpy.da.SearchCursor(feature_layer, field_name) as cursor:
            for row in cursor:
                if row[0] is None:  # Check if the value is null
                    null_count += 1
        # Append the field name and null count to the list
        field_null_counts.append({'Field': field_name, 'Null Count': null_count})

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(field_null_counts)

# Write the DataFrame to an Excel file
df.to_excel(output_file, index=False, engine='openpyxl')

# Confirm the file has been saved
print(f"Null value counts have been written to: {output_file}") """


import arcpy
import pandas as pd
import datetime
import os

# Define the path to your hosted feature layer
feature_layer = "https://webgis.bedfordcountyva.gov/arcgis/rest/services/OpenData/OpenDataBRWA/MapServer/2"  # Replace with your feature layer URL or path

# Get the current date in yyyymmdd format
current_date = datetime.datetime.now().strftime("%Y%m%d")

# Extract the feature layer name (if it's a path, extract the name from the file name)
layer_name = feature_layer.title
#print(layer_name)
print(layer_name)

# Define the output path for the Excel file
output_folder = r"C:\\Work\\Data_qc\\"  # Replace with your desired folder path

# Create the dynamic output filename using the date and feature layer name
output_excel = f"{current_date}_{layer_name}null_count.xlsx"
output_file = f"{output_folder}\\{output_excel}"

# Get the total number of features in the feature layer
total_features = int(arcpy.management.GetCount(feature_layer)[0])

# Create a list to hold the field names and null counts
field_null_counts = []

# Get the field names from the feature layer
fields = arcpy.ListFields(feature_layer)

# Iterate through each field to count the null values
for field in fields:
    field_name = field.name
    if field.type not in ['OID', 'Geometry']:  # Ignore OID and Geometry fields
        null_count = 0
        with arcpy.da.SearchCursor(feature_layer, field_name) as cursor:
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
print(f"Null value counts have been written to: {output_file}")


#---------------------------------------------------------------------------------------------

"""  # Extract the feature layer name (if it's a path, extract the name from the file name)
layer_name = feature_layer.split("\\")[-1].split(".")[0]  # This works for file paths, adjust for URLs if needed

# Define the output path for the Excel file
output_folder = r"C:\path\to\your\folder"  # Replace with your desired folder path

# Create the dynamic output filename using the date and feature layer name
output_excel = f"{current_date}_{layer_name}_null_values_count.xlsx"
output_file = f"{output_folder}\\{output_excel}"

# Get the total number of features in the feature layer
total_features = int(arcpy.management.GetCount(feature_layer)[0])

# Create a list to hold the field names, null counts, and percTotal values
field_null_counts = []

# Get the field names from the feature layer
fields = arcpy.ListFields(feature_layer)

# Iterate through each field to count the null values and calculate percTotal
for field in fields:
    field_name = field.name
    if field.type not in ['OID', 'Geometry']:  # Ignore OID and Geometry fields
        null_count = 0
        with arcpy.da.SearchCursor(feature_layer, field_name) as cursor:
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
print(f"Null value counts and percentages have been written to: {output_file}") """