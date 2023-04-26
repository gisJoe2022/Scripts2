# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: REST_Get_JSON_Request.py
# Description: Downloads RESTR peject FCs for post processing. Post processing is 
# selecting statewide proects by study area for map service. 
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


# rest parameters
params = {'f': 'json', 'where': '1=1', 'geometryType': 'esriGeometryPolygon', 'spatialRel': 'esriSpatialRelIntersects','outFields': '*', 'returnGeometry': 'true'}

# service ID. must enter each indevidually and run. I wasn't able to automate several IDs at once. 
# change jsontofeature_conversion number to match
num = '314'

#r = requests.get('https://gis.odot.state.or.us/arcgis1006/rest/services/transgis/data_catalog/MapServer/194/query', params)

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
# arcpro model does the rest of the processing
# \\emcgis\nas\GISDATA\Workgroups\GISPlanning\Transportation_Projects\TV_HWY\2022\TV_Hwy_2022_working.aprx