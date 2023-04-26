



geometry_layer_name = "name_of_the_layer_with_the_right_geometry"
attribute_layer_name = "name_of_the_layer_with_attributes_and_wrong_geometry"
common_field = "name_of_the_common_field"

# this will change the geometry of the second layer's underlying data, so back it up!

active_map = arcpy.mp.ArcGISProject("current").activeMap
geometry_layer = active_map.listLayers(geometry_layer_name)[0]
attribute_layer = active_map.listLayers(attribute_layer_name)[0]

# read the correct geometries and save them in a dictionary
# {common_field_value: shape}
cursor = arcpy.da.SearchCursor(geometry_layer, [common_field, "SHAPE@"])
shapes = dict([row for row in cursor])

# loop through the second layer and update the geometries
updated_features = []
with arcpy.da.UpdateCursor(attribute_layer, [common_field, "SHAPE@"]) as cursor:
    for row in cursor:
        try:
            new_shape = shapes[row[0]]
            # only update if the geometry is different, fill the updated_features list
            if not new_shape.equals(row[1]):
                cursor.updateRow([row[0], new_shape])
                updated_features.append(row[0])
        except KeyError:
            print("No new geometry found for feature with {} = {}".format(common_field, row[0]))


# build an SQL query of the updated_features, depending on whether common_field is a text field or not
if updated_features and isinstance(updated_features[0], str):
    sql = "{} IN ('{}')".format(common_field, "', '".join(updated_features))
else:
    sql = "{} IN ({})".format(common_field, ", ".join([str(uf) for uf in updated_features]))
# print the SQL query
print("Updated the geometry of {} features:\n{}".format(len(updated_features), sql))
