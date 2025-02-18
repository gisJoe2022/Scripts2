# Cityworks_UpdateURMDarea
# Created 08/03/2022
# Description: This script creates and updates URMD area polygon to support the SQL process of determining URMD status in, out, or partial.

import os, sys

cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import arcpy
arcpy.env.workspace = r"\\pwebgisapp1\GIS_Process_Scripts\ConnectionFiles\nutsde_roadsams_ASSETS.sde"
arcpy.env.overwriteOutput = True

# Import custom modules
import gbl, trktime
from modEmail_3_7 import Send

# Input Datasets
# Current URMD Area polygon. Maintained by A&T and FC needs to be updated annually as long as FC name changes. Current naming convention had last 2 digits of year at the end.
BOUNDARY_urmd = arcpy.MakeFeatureLayer_management(
    r"\\emcgis\NAS\LUTOPS\GIS\Admin\ArcCatalog\ITSGIS_GDB_Connections\washsde_production_SDE_PUBLIC.sde\BOUNDARY.URMD_23", 'URMDAREA', "URMD = 'Y'")

# Annexation areas used to erase areas out of URMD area. This may keep the output RoadsAMS FC better updated throughout the year.
BOUNDARY_annex = r"\\emcgis\NAS\LUTOPS\GIS\Admin\ArcCatalog\ITSGIS_GDB_Connections\washsde_RLIS_sde_public.sde\rlis.RLIS.RLIS_city_annexations"

# Output Datasets
RoadsAMS_ASSETS_URMD_Area = "URMD_Area"

Title = "Update URMD Area"
Message = ""
Error = 0
ScrptTimer = trktime.stopwatch()

# Change to MyEmailRyan for dev
EmailTo = gbl.MyEmailRyan
# # !!!!Change back to GroupEmail when moving to Prod!!!.
# EmailTo = gbl.GroupEmail

try:
    arcpy.analysis.Erase(BOUNDARY_urmd, BOUNDARY_annex, RoadsAMS_ASSETS_URMD_Area)

    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."

    Message = arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
    print(Message)

    Send(Title, Message, Error, EmailTo)

except:
    #send email with errors
    Error = Error + 1
    Message = arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

    Send(Title, Message, Error, EmailTo)