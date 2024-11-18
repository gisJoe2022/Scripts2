# ---------------------------------------------------------------------------
# LRS_AllMp.py
# Created on: 2011-07-18 14:24:25.00000
# Updated on: 2023-06-27 to support LRS revamp, deprecation of IRIS system, and python 3.7
# Description: Creates a point for every milepost in the county

# ---------------------------------------------------------------------------
import os, sys
cmd_folder = "\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy,  string, smtplib, trktime, gbl
arcpy.env.overwriteOutput = True

# Import custom modules
from DataTransfer.modMoveData_3_7 import GISDelete, GISCopy, GISCopyAlt, GISDeleteFeatures, GISAppendFeatures, GISTruncate
from DataTransfer.mod_lin_ref_IRIS_3_7 import IRIS_lin_ref
from DataTransfer.mod_local_3_7 import tmpGISwkspace
from modEmail_3_7 import Send

# Input data sources
RoadsAMS_Mileposts = gbl.RoadsAMS_Assets+"\\vw_Mileposts_ALL"
RoadsAMS_Mileposts_forLines = gbl.RoadsAMS_Assets+"\\vw_LRS_Milepost_Lines"

arcpy.env.qualifiedFieldNames = False

# Set the MResolution
arcpy.env.MResolution = 0.00005

# Set the MDomain
arcpy.env.MDomain = "-100 10000000"

Title = "All Mileposts Update Log"
Message = ""
Error = 0
ScrptTimer = trktime.stopwatch()

# Change to MyEmailRyan for dev
EmailTo = gbl.MyEmailRyan
# # !!!!Change back to GroupEmail when moving to Prod!!!.
# EmailTo = gbl.GroupEmail

try:

    GISlocal = tmpGISwkspace()
    myTemp=GISlocal.tempLoc
    Message=Message+GISlocal.msg.appendMessage
    # if arcpy.gp.exists(gbl.RdNet+gbl.vw_IRIS_Mileposts):
    if arcpy.gp.exists(RoadsAMS_Mileposts):
    # Clear Workspace Cache
        arcpy.ClearWorkspaceCache_management("")

        # Delete temp lrs_IRIS_allMP_WMAS
        Temp = GISDelete(myTemp+gbl.lrs_IRIS_allMP+"_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Delete temp LRS_allMP_2913
        print("Deleting production temp feature classes")
        Temp = GISDelete(myTemp+gbl.lrs_IRIS_allMP+"_2913")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Delete temp lrs_IRIS_allMP_lines_WMAS
        print("Deleting production temp feature classes")
        Temp = GISDelete(myTemp+gbl.lrs_IRIS_allMP_lines+"_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Delete production.streets.lrs_IRIS_allMP_WMAS
        print ("Deleting production temp feature classes")
        Temp = GISDelete(gbl.NpSTREETS+gbl.lrs_IRIS_allMP+"_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Delete production.streets.lrs_IRIS_allMP_lines_WMAS
        print ("Deleting production temp feature classes")
        Temp = GISDelete(gbl.NpSTREETS+gbl.lrs_IRIS_allMP_lines+"_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Delete temp lrs_IRIS_allMP
        print ("Deleting default feature classes")
        Temp = GISDelete(myTemp+gbl.lrs_IRIS_allMP)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Delete temp lrs_IRIS_allMP_lines
        print ("Deleting default feature classes")
        Temp = GISDelete(myTemp+gbl.lrs_IRIS_allMP_lines)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Delete temp vw_IRIS_Mileposts table
        print ("Deleting default feature classes")
        Temp = GISDelete(myTemp+gbl.vw_IRIS_Mileposts)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Delete temp vw_IRIS_Milepost_Lines table
        print ("Deleting default feature classes")
        Temp = GISDelete(myTemp+gbl.vw_IRIS_Milepost_Lines)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

       # Copies Milepost table to temp
        print ("Copy points data table to Temp")
        # Temp = GISCopyAlt(gbl.RdNet+gbl.vw_IRIS_Mileposts,myTemp+gbl.vw_IRIS_Mileposts)
        Temp = GISCopyAlt (RoadsAMS_Mileposts,myTemp+gbl.vw_IRIS_Mileposts)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Copies vw_LRS_Milepost_Lines view to temp
        print ("Copy lines data table to Temp")
        #Temp = GISCopyAlt(gbl.RdNet+gbl.vw_IRIS_Milepost_Lines,myTemp+gbl.vw_IRIS_Milepost_Lines)
        Temp = GISCopyAlt(RoadsAMS_Mileposts_forLines, myTemp+gbl.vw_IRIS_Milepost_Lines)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Create Milepost points from RoadAMS Milepost table
        # Create Milepost points from IRIS
        print ("Creating Milepost point geometry")
        mtemp = IRIS_lin_ref("POINT", myTemp, gbl.vw_IRIS_Mileposts, "Road_Number", "Milepost", "", "","")
        MpPts = mtemp.point
        Message = Message + mtemp.msg.appendMessage
        Error = Error + mtemp.msg.fail

        # Copies feature from event layer
        print ("Copy features from layer")
        Temp = GISCopy(MpPts,myTemp+gbl.lrs_IRIS_allMP)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        MpPts=None

        # Create Milepost lines
        print ("Creating Milepost line geometry")
        mptemp = IRIS_lin_ref("LINE",  myTemp, gbl.vw_IRIS_Milepost_Lines, "Road_Number", "Milepost", "EndMilepost", "","")
        MpLines = mptemp.line
        Message = Message + mptemp.msg.appendMessage
        Error = Error + mptemp.msg.fail

        # Copies feature from event layer
        print ("Copy features from layer")
        Temp = GISCopy(MpLines,myTemp+gbl.lrs_IRIS_allMP_lines)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        MpLines=None

    # Remove null geometry

        IRISpts="IRISpts"
        IRISlines="IRISlines"
        print ("Remove Null Geometry")
        arcpy.MakeFeatureLayer_management(myTemp+gbl.lrs_IRIS_allMP, IRISpts)
        arcpy.MakeFeatureLayer_management(myTemp+gbl.lrs_IRIS_allMP_lines, IRISlines)

        arcpy.SelectLayerByAttribute_management("IRISpts", "NEW_SELECTION", "LOC_ERROR IN ('ZERO LENGTH EXTENT', 'ROUTE MEASURE NOT FOUND', 'ROUTE NOT FOUND')")

        print ("Removing null geometry points")
        if int(arcpy.GetCount_management("IRISpts").getOutput(0))!=0:
            print ("Get point Count = " + str(int(arcpy.GetCount_management("IRISpts").getOutput(0))))
            arcpy.DeleteFeatures_management ("IRISpts")

        print ("Removing null geometry lines")
        arcpy.SelectLayerByAttribute_management("IRISlines", "NEW_SELECTION", "LOC_ERROR IN ('ZERO LENGTH EXTENT', 'MEASURE EXTENT OUT OF ROUTE MEASURE RANGE', 'ROUTE NOT FOUND')")

        if int(arcpy.GetCount_management("IRISlines").getOutput(0))!=0:
            print ("Get line Count = " + str(int(arcpy.GetCount_management("IRISlines").getOutput(0))))
            arcpy.DeleteFeatures_management ("IRISlines")

    # Delete production.streets.lrs_IRIS_allMP
        print ("Deleting nutsde production LRS_allMP feature class")
        Temp = GISDelete(gbl.NpSTREETS+gbl.LRS_allMP)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Copies feature from event layer
        print ("Copy points from temp FC to nutsde production LRS_allMP")
        Temp = GISCopyAlt(myTemp + gbl.lrs_IRIS_allMP, gbl.NpSTREETS + gbl.LRS_allMP)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Delete production.streets.LRS_allMP
        print ("Deleting nutsde production LRS_allMP_lines feature class")
        Temp = GISDelete(gbl.NpSTREETS + gbl.LRS_allMP_lines)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Copies feature from event layer
        print("Copy lines from temp FC to nutsde production LRS_allMP_lines")
        Temp = GISCopyAlt(myTemp+gbl.lrs_IRIS_allMP_lines,gbl.NpSTREETS+gbl.LRS_allMP_lines)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Reprojects FC's to WMAS and 2913
        print ("Reproject data")
        arcpy.Project_management(myTemp+gbl.lrs_IRIS_allMP, myTemp+gbl.lrs_IRIS_allMP+"_WMAS", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]","NAD_1983_HARN_To_WGS_1984","PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1553.424873737374],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Mile_US',1609.347218694438]]")
        arcpy.Project_management(myTemp+gbl.lrs_IRIS_allMP, myTemp+gbl.lrs_IRIS_allMP+"_2913", "PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',8202099.737532808],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Foot',0.3048]]", transform_method="", in_coor_system="PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1553.424873737374],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Mile_US',1609.347218694438]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")

     #  Copies feature from event layer
        print ("Copy reprojected lines from temp FC to nutsde production")
        Temp = GISCopyAlt(myTemp+gbl.lrs_IRIS_allMP+"_WMAS",gbl.NpSTREETS+gbl.lrs_IRIS_allMP+"_msGeom_WMAS" )
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail
# Stopped QC here
        print ("Deleting production temp feature classes")
        Temp = GISDelete(gbl.NpSTREETS+gbl.lrs_IRIS_allMP+"_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        # Delete production.streets.LRS_IRIS_allMP_2913
        print ("Deleting production temp feature classes")
        Temp = GISDelete(gbl.NpSTREETS + gbl.LRS_allMP + "_2913")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail
        print ("Copy ESRI points to Nutsde.production")
        Temp = GISCopyAlt(myTemp + gbl.lrs_IRIS_allMP + "_2913", gbl.NpSTREETS + gbl.LRS_allMP + "_2913")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        print ("project lines to WMAS")
        arcpy.Project_management(myTemp+gbl.lrs_IRIS_allMP_lines, myTemp+gbl.lrs_IRIS_allMP_lines+"_WMAS", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]","NAD_1983_HARN_To_WGS_1984","PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1553.424873737374],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Mile_US',1609.347218694438]]")

        print ("Copy ESRI lines to Nutsde.production")
        Temp = GISCopyAlt(myTemp+gbl.lrs_IRIS_allMP_lines+"_WMAS",gbl.NpSTREETS+gbl.lrs_IRIS_allMP_lines+"_msGeom_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

# THE FOLLOWING LAYERS IMPACT DATA USED THROUGHOUT THE ASSET BROWSER!

    # Delete features from distribution.Streets.
        print ("Delete distribution Features and Append 1")
        Temp =  GISTruncate(gbl.NdSTREETS+gbl.lrs_IRIS_allMP_lines+"_msGeom_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Append features to distribution.streets.
        Temp = GISAppendFeatures(gbl.NpSTREETS+gbl.lrs_IRIS_allMP_lines+"_msGeom_WMAS", gbl.NdSTREETS+gbl.lrs_IRIS_allMP_lines+"_msGeom_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Delete features from distribution.Streets.
        print ("Delete distribution Features and Append 2")
        Temp =  GISTruncate(gbl.NdSTREETS+gbl.lrs_IRIS_allMP+"_msGeom_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Append features to distribution.OPS.MinorBetterCandPts
        Temp = GISAppendFeatures(gbl.NpSTREETS+gbl.lrs_IRIS_allMP+"_msGeom_WMAS", gbl.NdSTREETS+gbl.lrs_IRIS_allMP+"_msGeom_WMAS")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Delete features from distribution.Streets.
        print ("Delete distribution Features and Append 3")
        Temp =  GISTruncate(gbl.NdSTREETS+gbl.LRS_allMP)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Append production features to distribution.Streets.LRS_allMP
      # Temp = GISAppendFeatures(gbl.NpSTREETS+gbl.lrs_IRIS_allMP, gbl.NdSTREETS+gbl.LRS_allMP)
        Temp = GISAppendFeatures(gbl.NpSTREETS + gbl.LRS_allMP, gbl.NdSTREETS + gbl.LRS_allMP)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Delete features from distribution.Streets.
        print ("Delete distribution Features and Append 4")
        # Temp =  GISTruncate(gbl.NdSTREETS+gbl.lrs_IRIS_allMP_lines)
        Temp = GISTruncate(gbl.NdSTREETS + gbl.LRS_allMP_lines)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    # Append features to distribution.OPS.MinorBetterCandPts
    #   Temp = GISAppendFeatures(gbl.NpSTREETS+gbl.lrs_IRIS_allMP_lines, gbl.NdSTREETS+gbl.lrs_IRIS_allMP_lines)
        GISAppendFeatures(gbl.NpSTREETS + gbl.LRS_allMP_lines, gbl.NdSTREETS + gbl.LRS_allMP_lines)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."
    print ("sending email")

# Send email with successful operations
    Send(Title, Message, Error, EmailTo)
    print ("email sent")
except:  #send email with errors

    Error = Error + 1
    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
    print(Message)
    Send(Title, Message, Error, EmailTo)