# Purpose: this script removes the RLIS UGB and adds WashCo Combined UGB to all the Comp Plan aprxs. 
# It iterates through the Pro project maps and adds Combined UGB from the SDE instance.

# 4/8/2021

# Reise> Washington County LRP GIS

import arcpy

aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NorthBethany_12_21.aprx')
# aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NorthBethany_01_11.aprx')
# aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NonStandard.aprx')
# aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_Standard.aprx')
for m in aprx.listMaps():
    rmvLyr = m.listLayers('Urban Growth Boundary')[0]
    m.removeLayer(rmvLyr)
    print("RLIS UGB removed from " + m.name)
    insertLyr = arcpy.mp.LayerFile(r"\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Urban Growth Boundary.lyrx")
    refLyr = m.listLayers('County Boundary*')[0]
    m.insertLayer(refLyr, insertLyr, 'AFTER')
    print("Combined UGB added to " + m.name)
    aprx.saveACopy(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NorthBethany_12_21_UGB_updated.aprx')
    
#aprx.saveACopy(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NorthBethany_01_11_UGB_updated.aprx')
#aprx.saveACopy(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NonStandard_UGB_updated.aprx')
# aprx.saveACopy(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_Standard_UGB_updated.aprx')
del aprx

print("done and done")