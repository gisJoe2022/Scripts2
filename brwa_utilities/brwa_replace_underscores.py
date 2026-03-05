# This script connects to ArcGIS Online and updates field aliases in feature services
# owned by a specific user, replacing underscores in field aliases with spaces.
# owner: Joe Hayes
# Date: 2025-07-01



from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com", "your_username", "your_password")

# Define the target owner
target_owner = "desired_owner_username"

# Search for feature services owned by the target user
items = gis.content.search(query=f'owner:{target_owner}', item_type='Feature Service')

# Counter for total changes
total_changes = 0

# Iterate through each item
for item in items:
    print(f"Processing item: {item.title}")
    flc = FeatureLayerCollection.fromitem(item)
    definition = flc.properties

    # Prepare update definition
    update_layers = []
    for layer in definition.layers:
        layer_id = layer.id
        fields = []
        for field in layer.fields:
            if "_" in field.alias:
                new_alias = field.alias.replace("_", " ")
                fields.append({"name": field.name, "alias": new_alias})
                total_changes += 1
        if fields:
            update_layers.append({"id": layer_id, "fields": fields})

    # Apply the update if there are changes
    if update_layers:
        update_dict = {"layers": update_layers}
        result = flc.manager.update_definition(update_dict)
        print(f"Updated aliases for item: {item.title}")
    else:
        print(f"No alias updates needed for item: {item.title}")

# Display total number of changes
print(f"\nTotal field alias changes made: {total_changes}")
