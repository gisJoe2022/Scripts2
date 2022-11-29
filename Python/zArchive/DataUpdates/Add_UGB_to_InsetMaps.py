# Purpose: this script adds the UGB to all the inset maps the the Comp Plan aprxs. It iterates through the Pro project inset maps and add RLIS UGB.

# 4/22/2020

# Reise> Washington County LRP GIS

import arcpy

#aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NonStandard.aprx')
aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_Standard.aprx')
for m in aprx.listMaps('Inset*'):
    insertLyr = arcpy.mp.LayerFile(r'\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Urban Growth Boundary.lyrx')
    refLyr = m.listLayers('County Boundary ')[0]
    m.insertLayer(refLyr, insertLyr, 'AFTER')
    print("UGB added to " + m.name)

aprx.save()
del aprx

print("done and done")
