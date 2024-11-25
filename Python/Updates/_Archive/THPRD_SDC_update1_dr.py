# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2021-06-07 14:33:41
"""
import arcpy
from sys import argv

def Model(zDistTHPRDsdc="C:\\Users\\josephh\\appdata\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\zWrite_washsde_distribution_boundary.sde\\distribution.BOUNDARY.thprd_sdc", prodTHPRDsdc="C:\\Users\\josephh\\appdata\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\washsde_production_boundary.sde\\production.BOUNDARY.thprd_sdc"):  # SDE THPRD SDC

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False


    # Process: Truncate Table (Truncate Table) (management)
    TruncateOutput = arcpy.management.TruncateTable(in_table=zDistTHPRDsdc)[0]

    # Process: Append (Append) (management)
    Updated_distTHPRDsdc = arcpy.management.Append(inputs=[prodTHPRDsdc], target=TruncateOutput, schema_type="NO_TEST", field_mapping="RECDIST \"RECDIST\" true true false 6 Text 0 0,First,#,production.BOUNDARY.thprd_sdc,RECDIST,0,6;SDC \"SDC\" true true false 255 Text 0 0,First,#,production.BOUNDARY.thprd_sdc,SDC,0,255;Name \"Name\" true true false 255 Text 0 0,First,#,production.BOUNDARY.thprd_sdc,Name,0,255;Note \"Note\" true true false 255 Text 0 0,First,#,production.BOUNDARY.thprd_sdc,Note,0,255;Ordinance \"Ordinance\" true true false 10 Text 0 0,First,#,production.BOUNDARY.thprd_sdc,Ordinance,0,10", subtype="", expression="")[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"\\emcgis\NAS\GISDATA\Workgroups\GISPlanning\GIS\GIS_Data_Updates\THPRD\THPRD_Pro.gdb", workspace=r"\\emcgis\NAS\GISDATA\Workgroups\GISPlanning\GIS\GIS_Data_Updates\THPRD\THPRD_Pro.gdb"):
        Model(*argv[1:])