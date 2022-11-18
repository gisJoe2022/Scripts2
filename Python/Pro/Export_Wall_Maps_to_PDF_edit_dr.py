# CP_NorthBethany2BatchExportAllMaps
# This script exports all of the Community Plan North Bethany 2 maps in the Community_Plan_Maps_NorthBethany_12_21.aprx, to PDFs

# Reise> Washington County LRP GIS

# April Fools 2020

import arcpy
from datetime import datetime
arcpy.env.overwriteOutput = True

# input Community Plan aprx. This one exports the NorthBethany maps.
aprx = arcpy.mp.ArcGISProject(r"\\emcgis\\NAS\\GISDATA\\Workgroups\\GISPlanning\\GIS\Website_Wall_Maps\\Wall_Maps_Pro\\Wall_Maps.aprx")

# output directory location for PDF's
printdate = datetime.today().strftime('%m/%d/%Y')
filenmedate = datetime.today().strftime('%Y_%m_%d')
outdir = r'\\emcgis\\NAS\\GISDATA\\Workgroups\\GISPlanning\\GIS\Website_Wall_Maps\\Wall_Maps_Pro\\PDF\\test\\'

# loop sets print date to current date and exports layouts to PDF
lyt = aprx.listLayouts()

# loop exports single page layouts enabled to PDF
for l in lyt:
    for elm in l.listElements("TEXT_ELEMENT"):
        if elm.name == "Document Info":
            elm.text = "Printed: " + printdate
            outfile = outdir + filenmedate + '_' + l.name
            print("exporting" + " " + l.name + " " + "to PDF")
            l.exportToPDF(outfile, 300, 'BETTER')

aprx.save()
del aprx

print("All maps exported and script finished. QC output PDFs")
