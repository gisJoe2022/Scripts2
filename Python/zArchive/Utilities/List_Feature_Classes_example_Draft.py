import arcpy
import os

arcpy.env.workspace = "\\Emcgis\\nas\\GISDATA\\Workgroups\\GISPlanning\\GIS\\GIS_Data_Requests\\2021\\2021-03-11_RTP_DEI_and_UPAA\\data_to_CWS.gdb"

datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)