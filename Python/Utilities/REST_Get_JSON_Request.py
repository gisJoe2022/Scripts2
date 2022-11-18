# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: Get_Request copy.py
# Description: Initiates a Get request to a REST service
# Purpose: Download publically available data.
# Author:      Joe Hayes
# Created:     12/22/2021
# ---------------------------------------------------------------------------

# modules
from typing import Text
import arcpy, os, requests, json

# workspace
arcpy.env.overwriteOutput = True
myfolder = arcpy.env.workspace
arcpy.env.workspace = "C:/TEMP1/rest_test"
arcpy.env.overwriteOutput = True

# parameters
params = {'f': 'json', 'where': '1=1', 'geometryType': 'esriGeometryPolygon', 'spatialRel': 'esriSpatialRelIntersects','outFields': '*', 'returnGeometry': 'true'}

# Variable 
num = '314'

#r = requests.get('https://gis.odot.state.or.us/arcgis1006/rest/services/transgis/data_catalog/MapServer/194/query', params)

 #for x in num:
fc = 'json_' + str(num)
url = 'https://gis.odot.state.or.us/arcgis1006/rest/services/transgis/data_catalog/MapServer/'

r = requests.get(url + str(num) + '/' + 'query', params)

print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('Starting')
print('Print url')
print(r.url)

restJson = r.json()
path = r"C:/TEMP1/rest_test/" + str(num) + '.json'
with open(path, 'w') as f:
     json.dump(restJson, f, indent=2)
               
print('starting json to feature')
arcpy.JSONToFeatures_conversion(path, os.path.join("rest_test.gdb", "314"))
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('Complete')