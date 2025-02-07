""" queries all the field in a fc and reports the number 
    of null values to a spreadsheet with the fc name at
    the end of the fielname.
      
    Author: Joe Hayes
    Date: 2/6/2025 """


from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import pandas as pd
from datetime import datetime
import os

# Connect to AGOL
gis = GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Access the hosted feature layer
feature_layer_url = "https://services3.arcgis.com/DXCmCcRcEQ793kMP/arcgis/rest/services/Gravity_Main_Sewer_2020/FeatureServer"
feature_layer = FeatureLayer(feature_layer_url)

# Specify the folder to save the spreadsheet
folder_path = r"\\nu\\gis\\Reports\Data_qc"

# Query all features
features = feature_layer.query(where="1=1", out_fields="*").features

# Extract field names
field_names = [field.name for field in feature_layer.properties.layer.field]

# Initialize a dictionary to store null counts
null_counts = {field: 0 for field in field_names}

# Count null values for each field
for feature in features:
    for field in field_names:
        if feature.attributes[field] is None:
            null_counts[field] += 1

# Calculate total number of features
total_features = len(features)

# Prepare data for the DataFrame
data = []
for field in field_names:
    null_count = null_counts[field]
    percent_null = (null_count / total_features) * 100
    data.append([field, null_count, total_features, percent_null])

# Convert the data to a DataFrame
df = pd.DataFrame(data, columns=['Field', 'Null Count', 'Total Features', 'Percent Null'])

# Get the feature layer name
feature_layer_name = feature_layer.properties.name

# Get the current date in yyyymmdd format
current_date = datetime.now().strftime("%Y%m%d")

# Ensure the folder exists, if not, create it
os.makedirs(folder_path, exist_ok=True)

# Save the DataFrame to an Excel file with the date and feature layer name in the specified folder
file_name = f"{current_date}_null_values_report_{feature_layer_name}.xlsx"
file_path = os.path.join(folder_path, file_name)
df.to_excel(file_path, index=False)

print(f"Report created successfully as {file_path}!")