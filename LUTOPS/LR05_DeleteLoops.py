# ---------------------------------------------------------------------------
# DeleteLoops.py
# Created on: 2011-07-11 11:48:34.00000
# Updated on: 2022-10-21 to support LRS revamp, deprecation of IRIS system, and python 3.7
# Description: Deletes problematic linear features for repossessing
# ---------------------------------------------------------------------------

#Allows importing of custom modules
import os, sys
cmd_folder = "\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy, string, smtplib

import gbl, trktime
from modEmail_3_7 import Send

# Local variables:
#***Source Data***
NpSTREETS_lrs_LOOPS = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS.lrs_LOOPS"
#***Final Product***
NpSTREETS_LRS_Routes = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS.LRS_Routes"

#***Intermediate Data***
lrs_LRS_Routes_Layer = "lrs_LRS_Routes_Layer"

Title = "Delete Loops from LRS Script"
Message = ""
Error = 0
EmailTo = gbl.MyEmailRyan
ScrptTimer = trktime.stopwatch()

arcpy.env.qualifiedFieldNames = False


try:
    # Process: Clear Workspace Cache
    arcpy.ClearWorkspaceCache_management("")

    # Process: Make lrs_IRIS_Routes a feature layer
    arcpy.management.MakeFeatureLayer(NpSTREETS_LRS_Routes, lrs_LRS_Routes_Layer, where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;IRIS_Road_Number IRIS_Road_Number VISIBLE NONE;Road_Name Road_Name HIDDEN NONE;Index_Number Index_Number HIDDEN NONE;Field Field HIDDEN NONE;Field1 Field1 HIDDEN NONE;Identifier Identifier HIDDEN NONE;Milepost_Begin Milepost_Begin HIDDEN NONE;Milepost_End Milepost_End HIDDEN NONE;Shape_Length Shape_Length VISIBLE NONE")

    # Process: Add Join to lrs_Loops
    arcpy.AddJoin_management(lrs_LRS_Routes_Layer, "IRIS_Road_Number", NpSTREETS_lrs_LOOPS, "IRIS_Road_Number", "KEEP_ALL")
    print ("Loops table joined")

    # Process: Select only loops
    arcpy.management.SelectLayerByAttribute(lrs_LRS_Routes_Layer, "NEW_SELECTION", 'production.STREETS.lrs_LOOPS.IRIS_Road_Number IS NOT NULL')

    # Process: Remove Join
    arcpy.RemoveJoin_management(lrs_LRS_Routes_Layer, "#")

    # Process: Delete Loops
    arcpy.DeleteFeatures_management(lrs_LRS_Routes_Layer)
    print ("Loops Deleted")
    print ("All Done!")

    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."


    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
    print (Message)

    Send(Title, Message, Error, EmailTo)

except:
    # sends email with errors
    Error = Error + 1
    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

    Send(Title, Message, Error, EmailTo)