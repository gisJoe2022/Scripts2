# ---------------------------------------------------------------------------
# CreateLRSRoutes.py
# Created on: 2011-07-08 13:49:29.00000
# Updated on: 2022-10-21 to support LRS revamp, deprecation of IRIS system, and python 3.7
# Description: Creates IRIS lrs and calibrates routes
# ---------------------------------------------------------------------------

#Allows importing of custom modules
import os, sys
cmd_folder = "\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy, string, smtplib

import gbl,trktime

from DataTransfer.modMoveData_3_7 import GISDelete, GISCopy, GISDeleteFeatures, GISAppendFeatures, GISTruncate
from modEmail_3_7 import Send

# Set the MResolution
arcpy.env.MResolution = 0.00005

# Set the MDomain
arcpy.env.MDomain = "-100 10000000"

# Local variables:

#***Source Data***
NpStreetsQC_LIDRoutes = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.LID_Route_Create"
NpSTREETS_CntyRouteCalib = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS.CntyRouteCalib"

#***Final Product***
NpSTREETSQC_LRS_Routes= "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.lrs_IRIS_Routes"
NpSTREETS_LRS_Routes= "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS.LRS_Routes"
NdSTREETS_LRS_Routes= "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NdStreets.sde\\distribution.STREETS.LRS_Routes"

#***Intermediate Data***
NpSTREETSQC_LRS_RTE_CREATE = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.LRS_RTE_CREATE"
NpSTREETSQC_LRS_RTE_CREATE_Miles = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.LRS_RTE_CREATE_Miles"
NpSTREETSQC_LRS_RTE_CREATE_Miles_Create = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.LRS_RTE_CREATE_Miles_Create"
WashStr_IRIS = "WashStr_IRIS"

Title = "Create IRIS Routes Script"
Message = ""
Error = 0

# # Change to MyEmailRyan for dev
# EmailTo = gbl.MyEmailRyan
# !!!!Change back to GroupEmail when moving to Prod!!!.
EmailTo = gbl.GroupEmail

ScrptTimer = trktime.stopwatch()

try:

# Deletes production.StreetsQC.IRIS_RTE_CREATE_Miles_Create
    print ("Delete production.StreetsQC.IRIS_RTE_CREATE_Miles_Create")
    Temp = GISDelete(NpSTREETSQC_LRS_RTE_CREATE_Miles_Create)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

# Deletes production.StreetsQC.IRIS_Rte_Miles_Create
    print ("Delete production.StreetsQC.IRIS_RTE_CREATE_Miles")
    Temp = GISDelete(NpSTREETSQC_LRS_RTE_CREATE_Miles)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

# Deletes production.StreetsQC.lrs_IRIS_Routes
    print ("Delete production.StreetsQC.lrs_IRIS_Routes")
    Temp = GISDelete(NpSTREETSQC_LRS_Routes)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Process: Clear Workspace Cache
    arcpy.ClearWorkspaceCache_management("")

    # Process: Delete Features
    Temp = GISTruncate(NpSTREETSQC_LRS_RTE_CREATE)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(NpStreetsQC_LIDRoutes, WashStr_IRIS, "IRIS_Road_Number IS NOT NULL AND IRIS_Road_Number <> '' AND IRIS_Road_Number <> ' '", "", "OBJECTID OBJECTID VISIBLE NONE;LOCALID LOCALID VISIBLE NONE;LEFTADD1 LEFTADD1 VISIBLE NONE;LEFTADD2 LEFTADD2 VISIBLE NONE;RGTADD1 RGTADD1 VISIBLE NONE;RGTADD2 RGTADD2 VISIBLE NONE;FDPRE FDPRE VISIBLE NONE;FNAME FNAME VISIBLE NONE;FTYPE FTYPE VISIBLE NONE;FDSUF FDSUF VISIBLE NONE;LZIP LZIP VISIBLE NONE;RZIP RZIP VISIBLE NONE;LCITY LCITY VISIBLE NONE;RCITY RCITY VISIBLE NONE;LCOUNTY LCOUNTY VISIBLE NONE;RCOUNTY RCOUNTY VISIBLE NONE;CFCC CFCC VISIBLE NONE;CLASS CLASS VISIBLE NONE;DRCT DRCT VISIBLE NONE;LEADZERO LEADZERO VISIBLE NONE;QUIRK QUIRK VISIBLE NONE;SIDE SIDE VISIBLE NONE;SOURCE SOURCE VISIBLE NONE;STRUC STRUC VISIBLE NONE;SUBAREA SUBAREA VISIBLE NONE;TYPE TYPE VISIBLE NONE;CREATEDATE CREATEDATE VISIBLE NONE;UPDATEDATE UPDATEDATE VISIBLE NONE;Alias Alias VISIBLE NONE;IRIS_Road_Number IRIS_Road_Number VISIBLE NONE;LOwner LOwner VISIBLE NONE;ROwner ROwner VISIBLE NONE;LMaintainer LMaintainer VISIBLE NONE;RMaintainer RMaintainer VISIBLE NONE;Other_Jur_Asset_Number Other_Jur_Asset_Number VISIBLE NONE;BegPtFeature BegPtFeature VISIBLE NONE;EndPtFeature EndPtFeature VISIBLE NONE;Comments Comments VISIBLE NONE;QC QC VISIBLE NONE;XY_Source XY_Source VISIBLE NONE;ResearchHistory ResearchHistory VISIBLE NONE;XY_CHK XY_CHK VISIBLE NONE;Attribute_CHK Attribute_CHK VISIBLE NONE;MSAG_CHK MSAG_CHK VISIBLE NONE;Adjusted Adjusted VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;F_ZLEV F_ZLEV VISIBLE NONE;T_ZLEV TZLEV VISIBLE NONE;Shape Shape VISIBLE NONE;Shape.len Shape.len VISIBLE NONE")

    # Process: Append
    #! To Do: database connection in field mapping needs to be changed to ArcPy database connection file or global
    arcpy.Append_management("WashStr_IRIS", NpSTREETSQC_LRS_RTE_CREATE, "NO_TEST", "beg_meas \"beg_meas\" true true false 8 Double 5 11 ,First,#;end_meas \"end_meas\" true true false 8 Double 5 11 ,First,#;Road_Name \"Road Name\" true true false 50 Text 0 0 ,First,#;IRIS_Road_Number \"IRIS_Road_Number\" true true false 8 Text 0 0 ,First,#,\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NutSDE - Dist.sde\\distribution.STREETS.WashStr,IRIS_Road_Number,-1,-1;Milepost_Begin \"Milepost_Begin\" true true false 8 Double 8 38 ,First,#;Milepost_End \"Milepost_End\" true true false 8 Double 8 38 ,First,#;GlobalID \"GlobalID\" false false true 38 GlobalID 0 0 ,First,#,\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NutSDE - Dist.sde\\distribution.STREETS.WashStr,GlobalID,-1,-1;SHAPE.len \"SHAPE.len\" false false true 0 Double 0 0 ,First,#,\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NutSDE - Dist.sde\\distribution.STREETS.WashStr,Shape.len,-1,-1", "")

    print ("Appended current Streets Data")
    # Process: Project
    arcpy.Project_management(NpSTREETSQC_LRS_RTE_CREATE, NpSTREETSQC_LRS_RTE_CREATE_Miles, "PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1553.424873737374],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Mile_US',1609.347218694438]]", "", "PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',8202099.737532808],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Foot',0.3048]]")
    print ("Reprojected Streets data")
    # Process: Create Routes
    arcpy.CreateRoutes_lr(NpSTREETSQC_LRS_RTE_CREATE_Miles, "IRIS_Road_Number", NpSTREETSQC_LRS_RTE_CREATE_Miles_Create, "LENGTH", "", "", "LOWER_RIGHT", "1", "0", "IGNORE", "INDEX")
    print ("Created IRIS Routes")
    # Process: Calibrate Routes
    # ****** Look into calibration step. Test this in ArcGIS Pro.
    arcpy.CalibrateRoutes_lr(NpSTREETSQC_LRS_RTE_CREATE_Miles_Create, "IRIS_Road_Number", NpSTREETS_CntyRouteCalib, "IRIS_Road_Number", "MilePost", NpSTREETSQC_LRS_Routes, "DISTANCE", "0 Unknown", "BETWEEN", "BEFORE", "AFTER", "IGNORE", "KEEP", "INDEX")
    print ("Calibrate IRIS routes")

    # Process: Delete Features (2)
    Temp = GISTruncate(NpSTREETS_LRS_Routes)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Process: Append (2)
    print ("Append routes to production.streets")
    Temp = GISAppendFeatures(NpSTREETSQC_LRS_Routes, NpSTREETS_LRS_Routes)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # # This block is commented out because the distribution FC NdSTREETS_LRS_Routes is updated in the final script AddLoops.py
    # # Process: Delete Features (2)
    # Temp = GISTruncate(NdSTREETS_LRS_Routes)
    # Message = Message + Temp.appendMessage
    # Error = Error + Temp.fail
    #
    # # Process: Append (2)
    # print("Append routes to distribution.streets")
    # Temp = GISAppendFeatures(NpSTREETS_LRS_Routes, NdSTREETS_LRS_Routes)
    # Message = Message + Temp.appendMessage
    # Error = Error + Temp.fail

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