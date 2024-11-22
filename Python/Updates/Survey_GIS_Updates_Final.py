# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NAME: Survey_GIS_Updates.py
# Description: Daily survey GIS data updates.  
# Purpose: 
# Author:      Joe Hayes
# Updated:     11/18/2024
# ---------------------------------------------------------------------------

import arcpy
import logging
import datetime
import os   

# enironment/workspace settings
arcpy.env.overwriteOutput = True


# variables
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
logfilename = f'{timestamp}_Survey.log'
logfilepath = fr'\\pwebgisapp1.co.washington.or.us\GIS_Process_Scripts\LUT_Survey\Logs\{logfilename}'

prod = "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\washsde_production_SURVEY.sde"
dist= "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\washsde_distribution_SURVEY.sde"
tprod = "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\tsqlgis1_production_SURVEY.sde"
tdist= "\\\\pwebgisapp1\\GIS_Process_Scripts\\ConnectionFiles\\tsqlgis1_distribution_SURVEY.sde"

#GroupEmail = "Joseph_Hayes@washingtoncountyor.gov"
#MyEmail = "Joseph_Hayes@washingtoncountyor.gov"
#Title = "Survey GIS Supdates Script"
#Message = ""
#Error = 0
#EmailTo = MyEmail
# generate time stamp for log file


# Configure the logger
logging.basicConfig(filename= logfilepath, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]')
#logging.basicConfig(filename= timestamp +'_app.log', level=logging.DEBUG, 
                    #format='%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]')

""" # Configure logging with date, time, and line number in the log file 
log_filename = f'process_{timestamp}.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',                     
                    handlers=[
                        logging.FileHandler(log_filename),                         
                        logging.StreamHandler()                     
                    ])
 """
 # sync corners
def sync_corners1():
    print("Syncing Corners")
    logging.info("Syncing Corners")
    arcpy.management.SynchronizeChanges(
        geodatabase_1 = tprod,
        in_replica="SURVEY.Corners_Rep", # will need to change back to ..._Rep2
        geodatabase_2 = tdist,
        in_direction="FROM_GEODATABASE1_TO_2",
        conflict_policy="IN_FAVOR_OF_GDB1",
        conflict_definition="BY_OBJECT",
        reconcile=""
    )
    logging.info("Syncing corners Complete")
    print("Syncing Corners Complete")

# syn TRS (townshi/range, sections, quarter section)   
def sync_trs1():
    print("Syncing TRS")
    logging.info("Syncing TRS")
    arcpy.management.SynchronizeChanges(
        geodatabase_1 = tprod,
        in_replica="SURVEY.surveyTownshipSectionQtrsec",
        geodatabase_2 = tdist,
        in_direction="FROM_GEODATABASE1_TO_2",
        conflict_policy="IN_FAVOR_OF_GDB1",
        conflict_definition="BY_OBJECT",
        reconcile=""
    )
    logging.info("Syncing TRS Complete")
    print("Syncing TRS Complete")

# Synch DLC
def sync_dlc1():
    print ("Syncing DLC")
    logging.info ("Syncing DLC")
    arcpy.management.SynchronizeChanges(
        geodatabase_1 = tprod,
        in_replica="survey.DLC_rep",
        geodatabase_2= tdist,
        in_direction="FROM_GEODATABASE1_TO_2",
        conflict_policy="IN_FAVOR_OF_GDB1",
        conflict_definition="BY_OBJECT",
        reconcile=""
    )
    logging.info("Syncing DLC Complete")
    print("Syncing DLC Complete")

 # snap corner filednotes points to corners
def update_fieldnotes1():
    print("Snapping Corner Fieldnotes")
    logging.info("Snapping Corner Fieldnotes")
    arcpy.edit.Snap(
        in_features= tprod + "\\production.SURVEY.corner_fieldnotes",
        snap_environment=[(tprod + "\\production.SURVEY.CORNERS", "VERTEX", "20 Meters")]
    )
    logging.info("Snapping Corner Fieldnotes Complete")
    print("Snapping Corner Fieldnotes Complete")

# recreate gps points from sql gps table
def gps_update1():
    print("Creating GPS Points")
    logging.info("Creating GPS Points")
    arcpy.management.XYTableToPoint(
        in_table= tprod + "\\production.survey.V_GPS",
        out_feature_class= tprod + "\\production.SURVEY.corner_GPS",
        x_field="easting_f",
        y_field="northing_f",
        z_field=None,
        coordinate_system='PROJCS["NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl",GEOGCS["GCS_North_American_1983_HARN",DATUM["D_North_American_1983_HARN",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",8202099.737532808],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-120.5],PARAMETER["Standard_Parallel_1",44.33333333333334],PARAMETER["Standard_Parallel_2",46.0],PARAMETER["Latitude_Of_Origin",43.66666666666666],UNIT["Foot",0.3048]];-111333600 -98152500 3048;-100000 10000;-100000 10000;3.28083989501312E-03;0.001;0.001;IsHighPrecision'
    )
    logging.info("Creating GPS Points Complete")
    print("Creating GPS Points Complete")
    print("Updates Complete")


# main script execution
def execute_all():
    defs1 = [sync_corners1, sync_trs1, sync_dlc1, update_fieldnotes1, gps_update1]
    for func in defs1:
        try:
            func()
        except Exception as e:
            logging.error(f'An error occured: {e}', exc_info=True)

execute_all()
logging.info("Updates Complete")
    