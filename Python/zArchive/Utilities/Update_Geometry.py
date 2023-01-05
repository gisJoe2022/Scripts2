# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: Update_Geometry.py
# Description: Uses a common attribute (primary key) to update the geometry
#              of one feature class from another. 
# Purpose:
# Author:      Johannes Lidner
# Created:     3/10/2021
# Copyright:   (c) 
# Licence:     <your licence>
# ---------------------------------------------------------------------------

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
with arcpy.da.UpdateCursor(attribute_layer, [common_field, "SHAPE@"]) as cursor:
    for row in cursor:
        try:
            new_shape = shapes[row[0]]
            cursor.updateRow([row[0], new_shape])
        except KeyError:
            print("No new geometry found for feature with {} = {}".format(common_field, row[0]))