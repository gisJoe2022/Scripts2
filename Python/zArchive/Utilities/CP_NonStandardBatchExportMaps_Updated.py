# CP_NonStandardBatchExportAllMaps
# This script exports all of the Community Plan Non Standard maps, both map series and single page layouts in the Community_Plan_Maps_NonStandard.aprx, to PDFs

# Reise> Washington County LRP GIS

# April Fools 2020

import arcpy
from datetime import datetime
arcpy.env.overwriteOutput = True

# input Community Plan aprx. This one exports the Non Standard maps.
aprx = arcpy.mp.ArcGISProject(r"\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_NonStandard.aprx")

# output directory location for PDF's
printdate = datetime.today().strftime('%m/%d/%Y')
# filenmedate = datetime.today().strftime('%Y_%m_%d')
outdir = r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\PDF\DRAFT\\'

# loop exports layouts with map series enabled to single page PDF
lyt = aprx.listLayouts()

for l in lyt:
     if not l.mapSeries is None:
         ms = l.mapSeries
         if ms.enabled:
            for elm in l.listElements("TEXT_ELEMENT"):
                if elm.name == "Date Printed":
                    elm.text = "Printed: " + printdate
                    ms = l.mapSeries
                    outfile = outdir + 'NonStandard_' + l.name # + '_' + filenmedate
                    print("exporting" + " " + l.name + " " + "to PDF")
                    ms.exportToPDF(outfile, "ALL", "", "PDF_MULTIPLE_FILES_PAGE_NAME", 300, "BEST")
print("-----All map series layouts exported to PDF's-----")

# loop exports single page layouts enabled to PDF
for l in lyt:
    if l.mapSeries is None:
        for elm in l.listElements("TEXT_ELEMENT"):
            if elm.name == "Date Prinited":
                elm.text = "Printed: " + printdate
                outfile = outdir + 'NonStandard_' + l.name # + '_' + filenmedate
                print("exporting" + " " + l.name + " " + "to PDF")
                l.exportToPDF(outfile, 300, 'BETTER')

print("-----All one page layouts exported to PDF's-----")

print("All maps exported and script finished. QC output PDFs")