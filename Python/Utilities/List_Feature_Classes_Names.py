# Set the workspace. List all of the feature classes

import arcpy

arcpy.env.workspace = r"\\emcgis\NAS\GISDATA\Workgroups\GISPlanning\GIS\GIS_Data_Updates_Pro\Scratch.gdb"
fcs = arcpy.ListFeatureClasses("*")

print(fcs)


