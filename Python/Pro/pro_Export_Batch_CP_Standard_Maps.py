# CP_StandardBatchExportAllMaps
# This script exports all of the Community Plan Standard maps, both map series and single page layouts in the Community_Plan_Maps_NonStandard.aprx, to PDFs

# Reise> Washington County LRP GIS

# April Fools 2020

import arcpy
from datetime import datetime
arcpy.env.overwriteOutput = 'True'

# input Community Plan aprx. This one exports the Non Standard maps.
aprx = arcpy.mp.ArcGISProject(r"\\Emcgis\NAS\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\Community_Plan_Maps_Standard.aprx")

# output directory location for PDF's
outdir = r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Community_Plan_Maps\PDF\DRAFT\\'
printdate = datetime.today().strftime('%m/%d/%Y')

# loop exports layouts with map series enabled to single multi PDFs. It also updates the text element print date, which was programed in because the dynamic text option of doing this only works when exporting is done manually from ArcPro.

lyt = aprx.listLayouts()

for l in lyt:
     if not l.mapSeries is None:
        ms = l.mapSeries
        if ms.enabled:
            ms = l.mapSeries
            for elm in l.listElements("TEXT_ELEMENT"):
                if elm.name == "Date Prinited":
                    elm.text = "Printed: " + printdate
                    outfile = outdir + 'Standard_' + l.name #+ '_' + date
                    print("exporting" + " " + l.name + " " + "to PDF")
                    ms.exportToPDF(outfile, "ALL", "", "PDF_MULTIPLE_FILES_PAGE_NUMBER", 300, "BEST")
print("-----All map series layouts exported to PDF's-----")

# loop exports single page layouts enabled to PDF. It also updates the text element print date, which was programed in because the dynamic text option of doing this only works when exporting is done manually from ArcPro.

for l in lyt:
    if l.mapSeries is None:
        for elm in l.listElements("TEXT_ELEMENT"):
            if elm.name == "Date Prinited":
                elm.text = "Printed: " + printdate
                outfile = outdir + 'Standard_' + l.name # + '_' + filenmedate
                print("exporting" + " " + l.name + " " + "to PDF")
                l.exportToPDF(outfile, 300, 'BETTER')
print("-----All one page layouts exported to PDF's-----")

print("All maps exported and script finished. QC output PDFs")