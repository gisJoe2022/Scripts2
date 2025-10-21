from arcgis.gis import GIS
from datetime import datetime
import os

# Function to search for items using a specific service URL and optional category
def find_items_using_service_url(gis, service_url, category=None):
    matching_items = []
    # Build the search query
    query = 'type:("Web Map" OR "Web Mapping Application")'
    if category:
        query += f' AND categories:"{category}"'
    items = gis.content.search(query, max_items=1000)
    for item in items:
        try:
            data = item.get_data()
            if data and service_url in str(data):
                matching_items.append((item.title, item.id))
        except Exception as e:
            print(f"Error reading item {item.title}: {e}")
    return matching_items

# User credentials and service URL
username = "brwa.sync_bedfordvagis"
password = "E&MBp^U@)4ybMWq"
service_url = "https://webgis.bedfordcountyva.gov/arcgis/rest/services/Locators/bedford_geocoder/GeocodeServer"

# Login to AGOL
gis = GIS("https://bedfordvagis.maps.arcgis.com", username, password)

# Prompt user for category (optional)
category = input("BRWA").strip()
category = category if category else None

# Find matching items
matches = find_items_using_service_url(gis, service_url, category)

# User-specified output directory
output_dir = input("S:\\BU_Databases\\logs\\")

# Create filename with date, hour, and minute
now = datetime.now()
filename = f"url_search_{now.strftime('%Y%m%d_%H%M')}.txt"
output_path = os.path.join(output_dir, filename)

# Write results to the specified text file
with open(output_path, "w") as f:
    for title, item_id in matches:
        f.write(f"Title: {title}, Item ID: {item_id}\n")
print(f"Results saved to {output_path}")
