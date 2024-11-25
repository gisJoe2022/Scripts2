# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2020-10-05 15:39:04
"""
import arcpy

def Model():  # SDE THPRD SDC

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    production_BOUNDARY_thprd_sdc = "Database Connections\\washsde_production_boundary.sde\\production.BOUNDARY.thprd_sdc"
    distribution_THPRD_SDC = "Database Connections\\zWRITE.washsde.Distribution.Boundary.sde\\distribution.BOUNDARY.thprd_sdc"

    # Process: Truncate Table (Truncate Table) (management)
    distribution_BOUNDARY_thprd_sdc_2_ = arcpy.management.TruncateTable(in_table=distribution_THPRD_SDC)[0]

    # Process: Append (Append) (management)
    if distribution_BOUNDARY_thprd_sdc_2_:
        distribution_BOUNDARY_thprd_sdc_updated = arcpy.management.Append(inputs=[production_BOUNDARY_thprd_sdc], target=distribution_BOUNDARY_thprd_sdc_2_, schema_type="NO_TEST", field_mapping="RECDIST \"RECDIST\" true true false 6 Text 0 0,First,#,C:\\Users\\josephh\\AppData\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\washsde_production_boundary.sde\\production.BOUNDARY.thprd_sdc,RECDIST,0,6;SDC \"SDC\" true true false 255 Text 0 0,First,#,C:\\Users\\josephh\\AppData\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\washsde_production_boundary.sde\\production.BOUNDARY.thprd_sdc,SDC,0,255;Name \"Name\" true true false 255 Text 0 0,First,#,C:\\Users\\josephh\\AppData\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\washsde_production_boundary.sde\\production.BOUNDARY.thprd_sdc,Name,0,255;Note \"Note\" true true false 255 Text 0 0,First,#,C:\\Users\\josephh\\AppData\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\washsde_production_boundary.sde\\production.BOUNDARY.thprd_sdc,Note,0,255;Ordinance \"Ordinance\" true true false 10 Text 0 0,First,#,C:\\Users\\josephh\\AppData\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\washsde_production_boundary.sde\\production.BOUNDARY.thprd_sdc,Ordinance,0,10", subtype="", expression="")[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"J:\Workgroups\GISPlanning\Data_Updates\Data_Updates.gdb", workspace=r"J:\Workgroups\GISPlanning\Data_Updates\Data_Updates.gdb"):
        Model()