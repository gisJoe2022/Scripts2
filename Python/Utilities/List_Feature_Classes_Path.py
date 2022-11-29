import arcpy
import os

arcpy.env.workspace = r"\\emcgis\NAS\GISDATA\Workgroups\GISPlanning\GIS\GIS_Data_Updates_Pro\Scratch.gdb"

datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)