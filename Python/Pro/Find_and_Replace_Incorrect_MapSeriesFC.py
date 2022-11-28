# Purpose: this script updates the maps in the Comp Plan project with the correct map series file to fix an error. It iterates through the Pro project maps finds the incorrect feature class and replaces with correct one
# 3/10/2020
# RR

import arcpy
aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps.aprx')
maps = aprx.listMaps()
for m in maps:
    print (m.name)
    m.updateConnectionProperties({'dataset': 'production.LAND.CP_Map_Tiles_G5'}, {'dataset': 'production.LAND.CP_Map_Tiles'})

aprx.save()
del aprx

print("done and done")