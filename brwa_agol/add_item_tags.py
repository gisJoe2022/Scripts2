

from arcgis.gis import GIS

# Step 1: Login to AGOL
gis = GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Step 2: Define owners and tag
owners = ["gisjoe2022_BedfordVAGIS"]
tag_to_add = "brwa"
tag_added_count = 0

# Step 3: Loop through each owner
for owner in owners:
    items = gis.content.search(query=f'owner:{owner}', max_items=1000)
    
    for item in items:
        if tag_to_add not in item.tags:
            print(f"Adding tag to item: {item.title}")
            new_tags = item.tags + [tag_to_add]
            item.update(item_properties={"tags": new_tags})
            tag_added_count += 1
        else:
            print(f"Item already has tag: {item.title}")

# Step 4: Print summary
print(f"\nTotal items updated with '{tag_to_add}' tag: {tag_added_count}")
