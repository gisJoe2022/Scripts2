# Set the workspace. List all of the feature classes

import arcpy

arcpy.env.workspace = "\\Emcgis\\nas\\GISDATA\\Workgroups\\GISPlanning\\GIS\\GIS_Data_Requests\\2021\\2021-03-11_RTP_DEI_and_UPAA\\data_to_CWS.gdb"
fcs = arcpy.ListFeatureClasses("*")

print(fcs)


