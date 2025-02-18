# ---------------------------------------------------------------------------
# CreateLIDRoutes.py
# Created on: 2011-07-08 09:14:31.00000
# Updated on: 2022-10-20 to support LRS revamp and python 3.7
# Description: Creates linear referencing routes on LocalID (street segment unique identifier) with the begin point =0 ending point=100 for each segment creating and lrs for the percentage of the segment
# ---------------------------------------------------------------------------

#Allows importing of custom modules
import os, sys
cmd_folder = "\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy, string, smtplib
arcpy.env.overwriteOutput = True

# Import custom modules
import gbl, trktime
from DataTransfer.modMoveData_3_7 import GISDelete, GISCopy, GISDeleteFeatures, GISTruncate, GISAppendFeatures, GISjoinFCtoTbl, CreateFieldMap
from DataTransfer.mod_lin_ref_IRIS_3_7 import IRIS_lin_ref
from modEmail_3_7 import Send

#Input Datasets
NdSTREETS_WashStr = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NdStreets.sde\\distribution.STREETS.WashStr"

#Intermediate Datasets
#----LID_Route_Create is used for preprocessing the streets linework to get it in a format for route creation
NpSTREETSQC_LID_Route_Create = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.LID_Route_Create"

#Output Datasets
NpSTREETS_LID_routes = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS.LID_routes"
NpSTREETSQC_LID_routes = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.LID_routes"
NdSTREETS_LID_routes = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NdStreets.sde\\distribution.STREETS.LID_routes"

Title = "LID Route Creation Script"
Message = ""
Error = 0

# # Change to MyEmailRyan for dev
# EmailTo = gbl.MyEmailRyan
# !!!!Change back to GroupEmail when moving to Prod!!!.
EmailTo = gbl.GroupEmail

ScrptTimer = trktime.stopwatch()

try:
    #Processing steps:
    # Update Str feature class in Nutsde.Production
    print ("Delete features from production")
    print (gbl.NpSTREETSQC+gbl.streets)
    Temp = GISTruncate(gbl.NpSTREETSQC+gbl.streets)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Appends features to production.STREETS_QC.str
    print ("Append features to distribution")
    print (gbl.MetroStr+gbl.streets)
    print (gbl.NpSTREETSQC+gbl.streets)
    Temp = GISAppendFeatures(gbl.MetroStr+gbl.streets, gbl.NpSTREETSQC+gbl.streets)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Delete LID Routes feature class (Must be deleted. Create routes does not overwrite)
    print ("Deleting feature class")
    print ("Delete features from production")
    print (NpSTREETSQC_LID_routes)
    Temp = GISTruncate(NpSTREETSQC_LID_routes)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Delete Features from LID_Route_Create (Delete features is used to keep schema in place, instead of having to rebuild the feature class)
    print ("Delete features from LID Route Create")
    Temp = GISDeleteFeatures(NpSTREETSQC_LID_Route_Create)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail
    print ("Deleted LID_Route_Create feature class")

    # Append latest Streets linework to LID_Route_Create for preprocessing
    print ("Append Streets linework to LID_Route_Create")
    Temp = GISAppendFeatures(gbl.NdSTREETS+gbl.WashStr, NpSTREETSQC_LID_Route_Create)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail
    print ("Appended Streets linework")

    print ("Join to get outside county lines")
    Temp = GISjoinFCtoTbl(gbl.NpSTREETSQC, gbl.streets, "localid", gbl.NpSTREETS, gbl.lrs_OutsideCounty, "LOCALID")
    lyrTemp= Temp.rtnText
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    fl = arcpy.gp.listFields(lyrTemp)

    for f in fl:
            fldNameLong = f.name
            fldType = f.type
            print (f.name)

    print ("Select layer attributes")
    arcpy.SelectLayerByAttribute_management(lyrTemp,"NEW_SELECTION", "tblvw_lrs_OutsideCounty.LOCALID IS NOT NULL")

    #Create field map
    print ("Create Field Map")
    Temp = CreateFieldMap(lyrTemp, gbl.NpSTREETSQC, gbl.streets, gbl.lrs_OutsideCounty)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail
    FMtemp=Temp.rtnText

    # Appends outside county localid's to dataset
    print ("Append outside county localids to dataset")
    Temp = GISAppendFeatures(lyrTemp, NpSTREETSQC_LID_Route_Create,FMtemp )
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Calculate LID_From field to 0. First calibration field for route creation.
    arcpy.CalculateField_management(NpSTREETSQC_LID_Route_Create, "LID_From", "0", "PYTHON_9.3")

    # Calculate LID_To field to 100. Second calibration field for route creation.
    arcpy.CalculateField_management(NpSTREETSQC_LID_Route_Create, "LID_To", "100", "PYTHON_9.3")
    print ("Calculated begin & end fields")
    # Create linear referenced routes
    arcpy.CreateRoutes_lr(NpSTREETSQC_LID_Route_Create, "LOCALID", NpSTREETSQC_LID_routes, "TWO_FIELDS", "LID_From", "LID_To", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    print ("Created LID Routes")

    # Delete Features from LID routes in Nutsde production
    print ("Delete features from production")
    print (gbl.NpSTREETSQC+gbl.streets)
    Temp = GISTruncate(NpSTREETS_LID_routes)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Appends new data to LID routes to Nutsde production
    print ("Append Streets linework to LID_Route_Create")
    Temp = GISAppendFeatures(NpSTREETSQC_LID_routes, NpSTREETS_LID_routes)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    print("Delete features from distribution")
    #print NdSTREETS_LID_routes
    Temp = GISTruncate(NdSTREETS_LID_routes)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Appends new data to LID routes to Nutsde production
    print ("Append Streets linework to LID_Route_Create")
    Temp = GISAppendFeatures(NpSTREETS_LID_routes, NdSTREETS_LID_routes)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    print ("All Done!")

    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."


    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
    print (Message)

    Send(Title, Message, Error, EmailTo)

except: # sends email with errors
    Error = Error + 1
    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

    Send(Title, Message, Error, EmailTo)