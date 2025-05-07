import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# Environment settings
arcpy.env.overwriteOutput = True

# Login to ArcGIS Online
gis = GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Retrieve the hosted feature service
item_id = "571b1d8fc62b418bb0a8d47763dd76d6"  # Replace with actual ID
item = gis.content.get(item_id)

if item and hasattr(item, "layers") and item.layers:
    print(f"Retrieved Feature Layer Collection: {item.title}")
    for index, layer in enumerate(item.layers):
        print(f"{index}: {layer.properties.name}")

    # Select the correct layer (modify index if needed)
    target_fc = item.layers[0]
    print(f"Using target feature layer: {target_fc.properties.name}")
else:
    raise ValueError("No layers found in the Feature Layer Collection.")

# Define the source feature class (local)
source_fc = r"C:\Work\test\test1.gdb\slrat_Copy"
source_fields = ["Assessment", "MeasDate"]

# Add spatial index for performance
arcpy.management.AddSpatialIndex(source_fc)

# Use a Search Cursor to iterate through the source feature class
with arcpy.da.SearchCursor(source_fc, ["SHAPE@", *source_fields]) as source_cursor:
    for source_row in source_cursor:
        source_geometry = source_row[0]  # ArcPy Geometry
        source_value = source_row[1]
        source_date = source_row[2]

        print(f"Processing Geometry: {source_geometry}")

        # Ensure geometry is in WGS 84 (EPSG:4326)
        spatial_ref = arcpy.SpatialReference(4326)
        if source_geometry.spatialReference.factoryCode != 4326:
            source_geometry = source_geometry.projectAs(spatial_ref)

        # Convert ArcPy geometry to ArcGIS JSON format
        source_geometry_json = {
            "x": source_geometry.centroid.X,
            "y": source_geometry.centroid.Y,
            "spatialReference": {"wkid": 4326}
        }

        print("Converted Geometry JSON:", source_geometry_json)

        # Query hosted feature layer using converted geometry
        query_result = target_fc.query(
            where="1=1",
            geometry=source_geometry_json,
            geometry_type="esriGeometryPoint",
            distance=30,
            #units="meters",
            return_geometry=True
        )

        features_to_update = query_result.features
        if features_to_update:
            for feature in features_to_update:
                feature.attributes["slrat_score"] = source_value
                feature.attributes["slrat_score_date"] = source_date

            # Update the hosted feature layer
            target_fc.edit_features(updates=features_to_update)
            print("Updated feature layer with new values.")

print("Field values updated successfully.")

""" 
import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayer


# Environment settings
arcpy.env.overwriteOutput = True

# Login to ArcGIS Online
gis = GIS("https://bedfordvagis.maps.arcgis.com", "j.hayes_bedfordvagis", "letrbuck4EO!")

# Retrieve the hosted feature service
item_id = "b962ffe1427043e29953dfe5e0d258bb" 
item = gis.content.get(item_id)

if item and hasattr(item, "layers") and item.layers:
    print(f"Retrieved Feature Layer Collection: {item.title}")
    for index, layer in enumerate(item.layers):
        print(f"{index}: {layer.properties.name}")

    # Select the correct layer (modify index if needed)
    target_fc = item.layers[0]
    print(f"Using target feature layer: {target_fc.properties.name}")
else:
    raise ValueError("No layers found in the Feature Layer Collection.")

# Define the source feature class (local)
source_fc = r"\\nu\gis\Projects\2025_Projects\202503_SL_RAT_Data\202503_SL_RAT_Data.gdb\Enhanced_Export_Bedford_Regional_Water_Authority_sum2024"
source_fields = ["Assessment", "MeasDate"]

# Add spatial index for performance
arcpy.management.AddSpatialIndex(source_fc)

# Use a Search Cursor to iterate through the source feature class
with arcpy.da.SearchCursor(source_fc, ["SHAPE@", *source_fields]) as source_cursor:
    for source_row in source_cursor:
        source_geometry = source_row[0]  # ArcPy Geometry
        source_value = source_row[1]
        source_date = source_row[2]

        print(f"Processing Geometry: {source_geometry}")

        # Convert ArcPy geometry to GeoJSON format for ArcGIS Online
        source_geometry_json = source_geometry.__geo_interface__
        print(f"Converted Geometry JSON: {source_geometry_json}")

        # Query hosted feature layer using converted geometry
        query_result = target_fc.query(
            where="1=1",
            geometry=source_geometry_json,
            distance=30,
            #unit="meters",
            return_geometry=True
        )

        features_to_update = query_result.features
        if features_to_update:
            for feature in features_to_update:
                feature.attributes["slrat_score"] = source_value
                feature.attributes["slrat_score_date"] = source_date

            # Update the hosted feature layer
            target_fc.edit_features(updates=features_to_update)
            print("Updated feature layer with new values.")

print("Field values updated successfully.")

 """