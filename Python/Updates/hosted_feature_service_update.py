# Description: This script connects to ArcGIS Online, 
# retrieves features from a source feature service, 
# and updates a target feature service with the retrieved features.
# date: 2023-10-03
# author: Joe Hayes


from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com", "your_username", "your_password")

# URL of the source feature service
source_url = "https://services.arcgis.com/your_source_service_url/FeatureServer/0"
source_layer = FeatureLayer(source_url)

# Query all features from the source layer
source_features = source_layer.query(where="1=1", out_fields="*").features

# URL of the target feature service
target_url = "https://services.arcgis.com/your_target_service_url/FeatureServer/0"
target_layer = FeatureLayer(target_url)

# Delete existing features in the target layer
target_layer.delete_features(where="1=1")

# Add the features from the source layer to the target layer
target_layer.edit_features(adds=source_features)

print("Data transfer complete!")