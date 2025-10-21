""" 

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
print(f"\nTotal items added to '{target_category}' category: {category_added_count}") """

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

import urllib3
from arcgis.gis import GIS

# Suppress HTTPS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Step 1: Login to AGOL
gis = GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Step 2: Define users and target category
users = ["d.henderson_BedfordVAGIS"]  # Add more users as needed  j.hayes_bedfordvagis
target_category = "BRWA"
category_added_count = 0

# Step 3: Search and update items for each user
for user in users:
    try:
        items = gis.content.search(query=f'owner:{user}', max_items=1000)
    except Exception as e:
        print(f"Error retrieving items for user '{user}': {e}")
        continue

    for item in items:
        try:
            if not item:
                print("Skipping null or inaccessible item.")
                continue

            current_categories = item.categories or []
            if target_category not in current_categories:
                print(f"Adding item to category '{target_category}': {item.title}")
                updated_categories = current_categories + [target_category]
                item.update(item_properties={"Categories": updated_categories})
                category_added_count += 1
            else:
                print(f"Item already in category '{target_category}': {item.title}")
        except Exception as e:
            print(f"Error processing item '{getattr(item, 'title', 'Unknown')}': {e}")
            continue

# Step 4: Print summary
print(f"\nTotal items added to '{target_category}' category: {category_added_count}")
