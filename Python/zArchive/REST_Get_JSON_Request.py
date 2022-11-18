# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: REST_Get_JSON_Request.py
# Description: downloads json from rest endpoint and converts to feature class in fgdb.
# Purpose: Download publicly available data.
# Author:      Joe Hayes
# Created:     12/22/2021
# Python 3
# Adding --------------------------------------------------
# ---------------------------------------------------------------------------

# modules
import arcpy, os, requests, json

# workspace
path = arcpy.env.workspace = 'J:\Workgroups\GISPlanning\Transportation_Projects\TV_HWY\Data\ODOT\JSON'
arcpy.env.overwriteOutput = True

# rest search parameters - grabs all records and feilds. rows must be <= max query in service properties
# break into multiple queries by OID if nessecary (ex 1-999, 1000-1999, ect) 
params = {'f': 'json', 'where': '1=1', 'geometryType': 'esriGeometryPolygon', 'spatialRel': 'esriSpatialRelIntersects','outFields': '*', 'returnGeometry': 'true'}

# --variables

# fgdb is current output location
fgdb = 'ODOT_JSON.gdb'
# service ID for json download request. appends to request.get url and fc name in jsontofeature below.
serv = '319'
print ("Requesting data from...")

#rest site 
r = requests.get('https://gis.odot.state.or.us/arcgis1006/rest/services/transgis/data_catalog/MapServer/' + serv + '/query', params)
print(r.url)

# json file save and convert to fc
restJson = r.json()
with open('rest.json', 'w') as f:
     json.dump(restJson, f, indent=2)
print("Saving data to GDB")
arcpy.JSONToFeatures_conversion('rest.json', os.path.join(fgdb, 'layer_'+ serv))
print ('Download Complete')