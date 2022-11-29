# Purpose: this script removes the RLIS archival county boundary shapefile from the Comp Plan aprxs. It iterates through the Pro project inset maps and adds RLIS City Limits from the SDE instance.

# 4/26/2020

# Reise> Washington County LRP GIS

import arcpy

#aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NonStandard.aprx')
aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_Standard.aprx')
for m in aprx.listMaps('Inset*'):
    insertLyr = arcpy.mp.LayerFile(r'\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Incorporated Area.lyrx')
    rmvLyr = m.listLayers('Incorporated Area')[0]
    m.removeLayer(rmvLyr)
    print("Incorporated Area removed from " + m.name)
    m.addLayer(insertLyr, 'BOTTOM')
    print("Updated Incorporated Area added to " + m.name)

aprx.save()
del aprx

print("done and done")
