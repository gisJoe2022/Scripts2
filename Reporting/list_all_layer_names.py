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
items = gis.content.search(query="*", max_items=10000)
print(f"Found {len(items)} items.")

# Extract layer names of feature services only
print("Extracting layer names of feature services...")
layer_names = []
for item in items:
    if item.type == 'Feature Service':
        if item.layers is not None:
            for layer in item.layers:
                layer_names.append(layer.properties.name)
print(f"Extracted {len(layer_names)} layer names.")

# Create a DataFrame
print("Creating DataFrame...")
df = pd.DataFrame(layer_names, columns=['Layer Name'])
print("DataFrame created successfully.")

# Define the name and location of the Excel file
file_name = '20250311_layer_list.xlsx'
file_location = r'S:\Projects\2025_Projects\202508_Layer_Cleanup\reports' + file_name

# Output to Excel
print(f"Saving layer names to Excel file at {file_location}...")
df.to_excel(file_location, index=False)
print(f"Layer names have been saved to {file_location}")
