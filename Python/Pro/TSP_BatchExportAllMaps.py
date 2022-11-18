# TSP_BatchExportAllMaps
# This script exports all of the adopted TSP User Guide maps both map series and single page layouts in the TSP_ReferenceGuide_Maps ArcGIS Pro aprx
# RR - Washington County LRP GIS
# 09/26/2019

import arcpy

# input TSP maps aprx
aprx = arcpy.mp.ArcGISProject(r"\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\COMP_PLAN\Transportation_Plan\TSP_ReferenceGuide_Maps\TSP_ReferenceGuide_Maps.aprx")

# output directory location for PDF's
outdir = r"\\Emcgis\NAS\GISDATA\\Workgroups\\GISPlanning\\COMP_PLAN\\Transportation_Plan\\TSP_ReferenceGuide_Maps\\PDF\\"

lyt = aprx.listLayouts()

# loop exports layouts with map serries enabled to single page PDF
for l in lyt:
    if not l.mapSeries is None:
        ms = l.mapSeries
        if ms.enabled:
            ms = l.mapSeries
            outfile = outdir + l.name
            print("exporting" + " " + l.name + " " + "to PDF")
            ms.exportToPDF(outfile, "ALL", "", "PDF_SINGLE_FILE", 300, "BEST")
print("-----All map series layouts exported to PDF's-----")

# loop exports single page layouts enabled to PDF
for l in lyt:
    if l.mapSeries is None:
        outfile = outdir + l.name
        print("exporting" + " " + l.name + " " + "to PDF")
        l.exportToPDF(outfile, 300, 'BETTER')
print("-----All one page layouts exported to PDF's-----")


print("All maps exported and script finished. QC output PDF's")