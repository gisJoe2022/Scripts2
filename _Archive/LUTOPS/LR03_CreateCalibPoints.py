# ---------------------------------------------------------------------------
# CreateCalibPoints.py
# Created: 2011-07-08 11:31:36.00000
# Updated: 2022-10-21 to support LRS revamp, deprecation of IRIS system, and python 3.7
# Description: Creates Calibration points for IRIS linear referencing routes
# ---------------------------------------------------------------------------
import os, sys
cmd_folder = "\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy, string, smtplib, trktime, gbl
from modEmail_3_7 import Send

# Input Datasets
RoadsAMS_Assets_Mileposts = gbl.RoadsAMS_Assets+"\\vw_Mileposts_ForCalibScript"
NpSTREETS_LID_routes = gbl.NpSTREETS+"LID_routes"

#Intermediate Datasets
# LRS_Calibration = "LRS_Calibration"

# Output Datasets
NpSTREETS_CntyRouteCalib = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS.CntyRouteCalib"

Title = "Create Calibration Points script"
Message = ""
Error = 0
ScrptTimer = trktime.stopwatch()

# Change to MyEmailRyan for dev
EmailTo = gbl.MyEmailRyan
# !!!!Change back to GroupEmail when moving to Prod!!!.
# EmailTo = gbl.GroupEmail

try:
    # Process: Clear Workspace Cache
    arcpy.ClearWorkspaceCache_management("")

    # Process: Delete CountyRouteCalib (need to rebuild schema because of XY calculate time issues)
    arcpy.Delete_management(NpSTREETS_CntyRouteCalib, "")
    print ("CountyRouteCalib deleted")

    # Process: Make Iris Calibration Point events
    LRS_Calibration = "LRS_Calibration"
    arcpy.lr.MakeRouteEventLayer(in_routes=NpSTREETS_LID_routes, route_id_field="LOCALID",
                                 in_table=RoadsAMS_Assets_Mileposts, in_event_properties="LOCALID; Point; LIDPct",
                                 out_layer=LRS_Calibration, offset_field="", add_error_field="NO_ERROR_FIELD",
                                 add_angle_field="NO_ANGLE_FIELD", angle_type="NORMAL", complement_angle="ANGLE",
                                 offset_direction="LEFT", point_event_type="POINT")
    print ("LRS event layer created")

    # Process: Copy Features (Copy Features) (management)
    arcpy.management.CopyFeatures(LRS_Calibration, NpSTREETS_CntyRouteCalib)
    print ("CountyRouteCalib created")

    # Process: Add XY Coordinates
    arcpy.AddXY_management(NpSTREETS_CntyRouteCalib)
    print ("Added XY data")

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