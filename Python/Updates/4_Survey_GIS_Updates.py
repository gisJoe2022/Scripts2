# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: Survey_GIS_Updates.py
# Description: Daily survey GIS data updates.  
# Purpose: 
# Author:      Joe Hayes
# Updated:     11/18/2024
# ---------------------------------------------------------------------------

import arcpy
print("Starting Updates")
# enironment/workspace settings
arcpy.env.overwriteOutput = True

# variables
prod = "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\washsde_production_SURVEY.sde"
dist= "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\washsde_distribution_SURVEY.sde"

tprod = "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\tsqlgis1_production_SURVEY.sde"
tdist= "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\tsqlgis1_distribution_SURVEY.sde"

GroupEmail = "Joseph_Hayes@washingtoncountyor.gov"
MyEmail = "Joseph_Hayes@washingtoncountyor.gov"
Title = "Survey GIS Updates Script"
Message = ""
Error = 0
EmailTo = MyEmail

# sync corners
print("Syncing Corners")
arcpy.management.SynchronizeChanges(
    geodatabase_1 = tprod,
    in_replica="SURVEY.Corners_Rep", # will need to change back to ..._Rep2
    geodatabase_2 = tdist,
    in_direction="FROM_GEODATABASE1_TO_2",
    conflict_policy="IN_FAVOR_OF_GDB1",
    conflict_definition="BY_OBJECT",
    reconcile="RECONCILE"
)
print("Syncing Corners Complete")

# syn TRS (townshi/range, sections, quarter section)
print("Syncing TRS")
arcpy.management.SynchronizeChanges(
    geodatabase_1 = tprod,
    in_replica="SURVEY.surveyTownshipSectionQtrsec",
    geodatabase_2 = tdist,
    in_direction="FROM_GEODATABASE1_TO_2",
    conflict_policy="IN_FAVOR_OF_GDB1",
    conflict_definition="BY_OBJECT",
    reconcile="RECONCILE"
)
print("Syncing TRS Complete")

# snap corner filednotes points to corners
print("Snapping Corner Fieldnotes")
arcpy.edit.Snap(
    in_features= tprod + "\\production.SURVEY.corner_fieldnotes",
    snap_environment=[(tprod + "\\production.SURVEY.CORNERS", "VERTEX", "20 Meters")]
)
print("Snapping Corner Fieldnotes Complete")

# recreate gps points from sql gps table
print("Creating GPS Points")
arcpy.management.XYTableToPoint(
    in_table= tprod + "\\production.survey.V_GPS",
    out_feature_class= tprod + "\\production.SURVEY.corner_GPS",
    x_field="easting_f",
    y_field="northing_f",
    z_field=None,
    coordinate_system='PROJCS["NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl",GEOGCS["GCS_North_American_1983_HARN",DATUM["D_North_American_1983_HARN",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",8202099.737532808],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-120.5],PARAMETER["Standard_Parallel_1",44.33333333333334],PARAMETER["Standard_Parallel_2",46.0],PARAMETER["Latitude_Of_Origin",43.66666666666666],UNIT["Foot",0.3048]];-111333600 -98152500 3048;-100000 10000;-100000 10000;3.28083989501312E-03;0.001;0.001;IsHighPrecision'
)
print("Creating GPS Points Complete")

# Truncate DLC table - donation land claim
print("Truncating DLC Table")
arcpy.management.TruncateTable(
    in_table= tdist + "\\distribution.SURVEY.DLC"
)
print("Truncating DLC Table Complete")

# Append production dlc to distribution dlc
print("Appending DLC Table")
with arcpy.EnvManager(preserveGlobalIds=False):
    arcpy.management.Append(
        inputs= tprod + "\\production.SURVEY.DLC",
        target= tdist + "\\distribution.SURVEY.DLC",
        schema_type="NO_TEST",
        field_mapping=r'CLAIM "CLAIM" true true false 2 Short 0 5,First,#,'
        + tprod + '\\production.SURVEY.DLC,CLAIM,-1,-1;LASTNAME "LASTNAME" true true false 30 Text 0 0,First,#,'
        + tprod + '\\production.SURVEY.DLC,LASTNAME,0,30;FIRSTNAME "FIRSTNAME" true true false 30 Text 0 0,First,#,'
        + tprod + '\\production.SURVEY.DLC,FIRSTNAME,0,30;BOTHNAMES "BOTHNAMES" true true false 30 Text 0 0,First,#,'
        + tprod + '\\production.SURVEY.DLC,BOTHNAMES,0,30;GlobalID "GlobalID" false false true 38 GlobalID 0 0,First,#',
        subtype="",
        expression="",
        match_fields=None,
        update_geometry="NOT_UPDATE_GEOMETRY"
    )
print("Appending DLC Table Complete")
print("Updates Complete")