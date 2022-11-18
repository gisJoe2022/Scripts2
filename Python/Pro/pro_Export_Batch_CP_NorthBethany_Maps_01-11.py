# CP_NonStandardBatchExportAllMaps
# This script exports all of the Community Plan North Bethany maps in the Community_Plan_Maps_NorthBethany.aprx, to PDFs

# Reise> Washington County LRP GIS

# April Fools 2020

import arcpy
from datetime import datetime
arcpy.env.overwriteOutput = True

# input Community Plan aprx. This one exports the NorthBethany maps.
aprx = arcpy.mp.ArcGISProject(r"\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NorthBethany_01_11.aprx")

# output directory location for PDF's
printdate = datetime.today().strftime('%m/%d/%Y')
# filenmedate = datetime.today().strftime('%Y_%m_%d')
outdir = r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\PDF\DRAFT\\'

# loop sets print date to current date and exports layouts to PDF
lyt = aprx.listLayouts()

# loop exports single page layouts enabled to PDF
for l in lyt:
    for elm in l.listElements("TEXT_ELEMENT"):
        if elm.name == "Date Prinited":
            elm.text = "Printed: " + printdate
            outfile = outdir + 'NorthBethany_' + l.name# + '_' + filenmedate
            print("exporting" + " " + l.name + " " + "to PDF")
            l.exportToPDF(outfile, 300, 'BETTER')

aprx.save()
del aprx

print("All maps exported and script finished. QC output PDFs")