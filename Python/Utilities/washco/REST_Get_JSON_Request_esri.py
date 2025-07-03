# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: REST_Get_JSON_Request_new.py
# Description: Initiates a Get request to a REST service
# Purpose: Download publically available data.
# Author:      ESRI
# Created:     5/3/2022
# Originator: https://support.esri.com/en/technical-article/000019645
# ---------------------------------------------------------------------------

# modules
import urllib.parse, urllib.request, os, arcpy, json

arcpy.env.overwriteOutput = True

# # Specify built-in Portal for ArcGIS account credentials
# username = "portaluser"
# password = "portalpassword"

# tokenURL = 'https://server.domain.com/portal/sharing/rest/generateToken/'
# params = {'f': 'pjson', 'username': username, 'password': password, 'referer': 'https://server.domain.com'}

# data = urllib.parse.urlencode(query=params).encode('utf-8')
# req = urllib.request.Request(tokenURL, data)
# response = urllib.request.urlopen(req)

# data = json.loads(response.read())
# token = data['token']

# Specify REST URL for service JSON to be returned
url = "https://server.domain.com/server/rest/services/servicename/MapServer/0/query?"

params = {'where': '1=1',
          'geometryType': 'esriGeometryEnvelope',
          'spatialRel': 'esriSpatialRelIntersects',
          'relationParam': '',
          'outFields': '*',
          'returnGeometry': 'true',
          'geometryPrecision': '',
          'outSR': '',
          'returnIdsOnly': 'false',
          'returnCountOnly': 'false',
          'orderByFields': '',
          'groupByFieldsForStatistics': '',
          'returnZ': 'false',
          'returnM': 'false',
          'returnDistinctValues': 'false',
          'f': 'pjson',
          'token': token
          }

encode_params = urllib.parse.urlencode(params).encode("utf-8")

response = urllib.request.urlopen(url, encode_params)
json = response.read()

with open("mapservice.json", "wb") as ms_json:
    ms_json.write(json)

ws = os.getcwd() + os.sep
arcpy.JSONToFeatures_conversion("mapservice.json", ws + "mapservice.shp", )