# Purpose: this script adds the UGB to all the inset maps the the Comp Plan aprxs. It iterates through the Pro project inset maps and add RLIS UGB.

# 5/26/2020

# Reise> Washington County LRP GIS

import arcpy, os

#Input aprx variable. Change as needed.
#aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_Standard.aprx')
#aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NonStandard.aprx')
#aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NorthBethany_01_11.aprx')
aprx = arcpy.mp.ArcGISProject(r'\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NorthBethany_12_21.aprx')

oFileHeaders = "Map Name,Layer Name,Data Source"
#Output CSV. Change to aprx variable file name.
#f = open(r"\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Documents_Tables\Standard_aprx_2020_8_11.csv", "w")
#f = open(r"\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Documents_Tables\NonStandard_aprx_2020_8_12.csv", "w")
#f = open(r"\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Documents_Tables\NorthBethany_01_11.aprx_2020_8_12.csv", "w")
f = open(r"\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Documents_Tables\NorthBethany_12_21_aprx_2020_8_12.csv", "w")

f.write(oFileHeaders+"\n")

for m in aprx.listMaps():
    #print(m.name)
    for l in m.listLayers():
        if l.supports('DATASOURCE'):
            mapNme = m.name
            lryNme = l.name
            dSource = l.dataSource
            f.write(mapNme + "," + lryNme + "," + dSource)
            f.write('\n')

print("done and done")
