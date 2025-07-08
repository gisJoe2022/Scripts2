

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from arcgis.gis import GIS


# Step 1: Login to AGOL
gis = GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Step 2: Define users and target category
users = ["d.henderson_BedfordVAGIS"]  # Add more users as needed  j.hayes_bedfordvagis
target_category = "BRWA"
category_added_count = 0

# Step 3: Search and update items for each user
for user in users:
    items = gis.content.search(query=f'owner:{user}', max_items=1000)
    
    for item in items:
        current_categories = item.categories or []
        if target_category not in current_categories:
            print(f"Adding item to category '{target_category}': {item.title}")
            updated_categories = current_categories + [target_category]
            item.update(item_properties={"categories": updated_categories})
            category_added_count += 1
        else:
            print(f"Item already in category '{target_category}': {item.title}")

# Step 4: Print summary
print(f"\nTotal items added to '{target_category}' category: {category_added_count}")

