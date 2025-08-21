from arcgis.gis import GIS
import csv
import os
from datetime import datetime

# User credentials and parameters
username = "j.hayes_bedfordvagis"
password = "letrbuck4EO!"
web_map_title = "BRWA Engineering"
target_group_layer_name = "BRWA Layers"
output_folder = r"S:\BU_Databases\2025\general"

# Generate timestamp for filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"layer_urls_{timestamp}.csv"

# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com", username, password)
print("Logged in as:", gis.users.me.username)

# Search for the web map
web_maps = gis.content.search(query=web_map_title, item_type="Web Map", max_items=1)
if not web_maps:
    print("Web map not found.")
    exit()

web_map = web_maps[0]
web_map_data = web_map.get_data()

# Find the specific group layer
group_layer = None
for layer in web_map_data.get("operationalLayers", []):
    if layer.get("title") == target_group_layer_name and "layers" in layer:
        group_layer = layer
        break

if not group_layer:
    print(f"Group layer '{target_group_layer_name}' not found.")
    exit()

# Recursively extract URLs from all nested layers
def extract_all_urls(layer_group):
    urls = []
    for layer in layer_group.get("layers", []):
        if "url" in layer:
            urls.append(layer["url"])
        if "layers" in layer:  # nested group layer
            urls.extend(extract_all_urls(layer))
    return urls
layer_urls = extract_all_urls(group_layer)

# Save to CSV with properly quoted URLs
output_path = os.path.join(output_folder, output_filename)
with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    for url in layer_urls:
        writer.writerow([url])

print(f"Layer URLs saved to {output_path}")




""" 
from arcgis.gis import GIS
import csv
import os
from datetime import datetime

# User credentials and parameters
username = "j.hayes_bedfordvagis"
password = "letrbuck4EO!"
web_map_title = "BRWA Engineering"
target_group_layer_name = "BRWA Water"
output_folder = r"S:\BU_Databases\2025\water"
# Generate timestamp for filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"layer_urls_{timestamp}.csv"


# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com", username, password)
print("Logged in as:", gis.users.me.username)

# Search for the web map
web_maps = gis.content.search(query=web_map_title, item_type="Web Map", max_items=1)
if not web_maps:
    print("Web map not found.")
    exit()

web_map = web_maps[0]
web_map_data = web_map.get_data()

# Find the specific group layer
group_layer = None
for layer in web_map_data.get("operationalLayers", []):
    if layer.get("title") == target_group_layer_name and "layers" in layer:
        group_layer = layer
        break

if not group_layer:
    print(f"Group layer '{target_group_layer_name}' not found.")
    exit()

# Recursively extract URLs from all nested layers
def extract_all_urls(layer_group):
    urls = []
    for layer in layer_group.get("layers", []):
        if "url" in layer:
            urls.append(layer["url"])
        if "layers" in layer:  # nested group layer
            urls.extend(extract_all_urls(layer))
    return urls

layer_urls = extract_all_urls(group_layer)

# Save to CSV
output_path = os.path.join(output_folder, output_filename)
# Format URLs as quoted and comma-separated
quoted_urls = [f'"{url}"' for url in layer_urls]
with open(output_path, mode='w', newline='') as file:
    for url in layer_urls:
        file.write(f'"{url}", \n')

print(f"Layer URLs saved to {output_path}")

 """


""" 
from arcgis.gis import GIS
import csv
import os

# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com", username, password)
print("Logged in as:", gis.users.me.username)

# Search for the web map
web_maps = gis.content.search(query=web_map_title, item_type="Web Map", max_items=1)
if not web_maps:
    print("Web map not found.")
    exit()

web_map = web_maps[0]
web_map_data = web_map.get_data()

# Find the specific group layer
group_layer = None
for layer in web_map_data.get("operationalLayers", []):
    if layer.get("title") == target_group_layer_name and "layers" in layer:
        group_layer = layer
        break

if not group_layer:
    print(f"Group layer '{target_group_layer_name}' not found.")
    exit()

# Recursively extract URLs from all nested layers
def extract_all_urls(layer_group):
    urls = []
    for layer in layer_group.get("layers", []):
        if "url" in layer:
            urls.append(layer["url"])
        if "layers" in layer:  # nested group layer
            urls.extend(extract_all_urls(layer))
    return urls

layer_urls = extract_all_urls(group_layer)

# Save to CSV
output_path = os.path.join(output_folder, output_filename)
with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Layer URL"])
    for url in layer_urls:
        writer.writerow([url])

print(f"Layer URLs saved to {output_path}")

 """



""" 
# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com", username, password)
print("Logged in as:", gis.users.me.username)

# Search for the web map
web_maps = gis.content.search(query=web_map_title, item_type="Web Map", max_items=1)
if not web_maps:
    print("Web map not found.")
    exit()

web_map = web_maps[0]
web_map_data = web_map.get_data()

# Find the specific group layer
group_layer = None
for layer in web_map_data.get("operationalLayers", []):
    if layer.get("title") == target_group_layer_name and "layers" in layer:
        group_layer = layer
        break

if not group_layer:
    print(f"Group layer '{target_group_layer_name}' not found.")
    exit()

# Extract URLs from the group layer's sublayers
def extract_urls_from_group(group):
    urls = []
    for sublayer in group.get("layers", []):
        if "url" in sublayer:
            urls.append(sublayer["url"])
    return urls

layer_urls = extract_urls_from_group(group_layer)

# Save to CSV
output_path = os.path.join(output_folder, output_filename)
with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Layer URL"])
    for url in layer_urls:
        writer.writerow([url])

print(f"Layer URLs saved to {output_path}")
 """