# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: Get_Request.py
# Description: Initiates a Get request to a REST service
# Purpose: Download publically available data.
# Author:      Joe Hayes
# Created:     12/22/2021
# ---------------------------------------------------------------------------

# modules
import arcpy, os, requests, json

# workspace
arcpy.env.workspace = "C:/TEMP1/rest_test"
arcpy.env.overwriteOutput = True

# parameters
params = {'f': 'json', 'where': '1=1', 'geometryType': 'esriGeometryPolygon', 'spatialRel': 'esriSpatialRelIntersects','outFields': '*', 'returnGeometry': 'true'}

print ("Requesting data from...")
r = requests.get('https://gis.odot.state.or.us/arcgis1006/rest/services/transgis/data_catalog/MapServer/194/query', params)
print(r.url)

#json = Text
restJson = r.json()
path = r"C:\TEMP1\rest_test"
with open(path, 'w') as f:
     json.dump(restJson, f, indent=2)
#with open(path, 'r+') as f:
     #json.dump(restJson, f, indent=2)
print("Saving data to GDB")
arcpy.JSONToFeatures_conversion("rest.json", os.path.join("rest_test.gdb",  "layer_194"))
print ("Download Complete")