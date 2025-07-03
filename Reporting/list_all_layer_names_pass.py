# Script to list all layer names from ArcGIS Online (AGOL) feature services
## This script connects to AGOL, retrieves all items, filters for feature services,
## and saves the layer names to an Excel file.



# Import necessary libraries
import pandas as pd
from arcgis.gis import GIS

# Define your AGOL credentials
username = 'j.hayes_bedfordvagis'
password = 'letrbuck4EO!'

# Log in to AGOL
print("Logging in to AGOL...")
gis = GIS("https://bedfordvagis.maps.arcgis.com", username, password)
print("Logged in successfully.")

# Get all items in the organization
print("Searching for all items in the organization...")
items = gis.content.search(query="BRWA", max_items=10000)
print(f"Found {len(items)} items.")

# Extract layer names, URLs, owner, type, and field count of feature services only
print("Extracting layer names, URLs, owners, types, and field counts of feature services...")
layer_info = []
for item in items:
    if item.type == 'Feature Service':
        if item.layers is not None:
            for layer in item.layers:
                layer_name = layer.properties.name
                layer_url = layer.url
                owner = item.owner
                item_type = item.type
                # Count the number of fields in the layer
                field_count = len(layer.properties.fields) if hasattr(layer.properties, "fields") else 0
                layer_info.append({
                    'Layer Name': layer_name,
                    'Path': layer_url,
                    'Owner': owner,
                    'Type': item_type,
                    'field_count': field_count
                })
print(f"Extracted {len(layer_info)} layers.")

# Create a DataFrame
print("Creating DataFrame...")
df = pd.DataFrame(layer_info, columns=['Layer Name', 'Path', 'Owner', 'Type', 'field_count'])
print("DataFrame created successfully.")

# Define the name and location of the Excel file
file_name = '20250606_layer_list.xlsx'
file_location = r'S:\Projects\2025_Projects\202508_Layer_Cleanup\reports\reports' + file_name

# Output to Excel
print(f"Saving layer names to Excel file at {file_location}...")
df.to_excel(file_location, index=False)
print(f"Layer names have been saved to {file_location}")

""" # Optional: Clean up large objects to free memory (not usually necessary for scripts of this size)
del items
del layer_info
del df """
