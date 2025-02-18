# Cityworks_Update_WashCoRoads.py
# Created 2022/1/27
# Description: Creates and updates road centerline FC in the RoadsAMS_Assets database for use as an asset feature type in Cityworks.

#Allows importing of custom modules
import os, sys
cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy
from arcpy import env

# Import custom modules
import gbl, trktime

from modEmail_3_7 import Send

# Process: Clear Workspace Cache
arcpy.ClearWorkspaceCache_management("")

# Input Datasets
production_streets_WashStr_2913_vw = gbl.NpSTREETS+gbl.WashStr_2913
RoadsAMS_ASSETS_Ops_WashCo_Roads = gbl.RoadsAMS_Assets+'Ops_WashCo_Roads'
URMD_Area = gbl.RoadsAMS_Assets+gbl.URMD_Area_RoadsAMS

Title = "Update All County Roads for Cityworks Script"
Message = ""
Error = 0

# # Change to MyEmailRyan for dev
# EmailTo = gbl.MyEmailRyan
# !!!!Change back to GroupEmail when moving to Prod!!!.
EmailTo = gbl.GroupEmail

ScrptTimer = trktime.stopwatch()

try:
    # Exports out comparison table for the previous month of RoadsAMS_ASSETS_Ops_WashCo_Roads prior to updating
    arcpy.TableToTable_conversion (RoadsAMS_ASSETS_Ops_WashCo_Roads, gbl.RoadsAMS_Assets, 'Ops_WashCo_Roads_PreviousMonth')
    # Deletes features from RoadsAMS_ASSETS_Ops_WashCo_Roads
    arcpy.DeleteFeatures_management(RoadsAMS_ASSETS_Ops_WashCo_Roads)
    print('Features from RoadsAMS_ASSETS_Ops_WashCo_Roads deleted')

    # Makes a feature layer from WashStr_2913 querying County owned and maintained roads and URMD functional classifications
    streets_WashStr_2913_vw_Laye = "streets.WashStr_2913_vw_Laye"
    arcpy.management.MakeFeatureLayer(in_features=production_streets_WashStr_2913_vw,
                                      out_layer=streets_WashStr_2913_vw_Laye,
                                      where_clause="(LOwner IN ('Washington', 'Washington Co') Or ROwner IN ('Washington', 'Washington Co') Or LMaintainer IN ('Washington', 'Washington Co') Or RMaintainer IN ('Washington', 'Washington Co') Or IRIS_Road_Number = '194380')",
                                      workspace="",
                                      field_info="OBJECTID OBJECTID VISIBLE NONE;LOCALID LOCALID VISIBLE NONE;FullStreetName FullStreetName VISIBLE NONE;LEFTADD1 LEFTADD1 VISIBLE NONE;LEFTADD2 LEFTADD2 VISIBLE NONE;RGTADD1 RGTADD1 VISIBLE NONE;RGTADD2 RGTADD2 VISIBLE NONE;FDPRE FDPRE VISIBLE NONE;FNAME FNAME VISIBLE NONE;FTYPE FTYPE VISIBLE NONE;FDSUF FDSUF VISIBLE NONE;LZIP LZIP VISIBLE NONE;RZIP RZIP VISIBLE NONE;LCITY LCITY VISIBLE NONE;RCITY RCITY VISIBLE NONE;LCOUNTY LCOUNTY VISIBLE NONE;RCOUNTY RCOUNTY VISIBLE NONE;CFCC CFCC VISIBLE NONE;CLASS CLASS VISIBLE NONE;DRCT DRCT VISIBLE NONE;LEADZERO LEADZERO VISIBLE NONE;QUIRK QUIRK VISIBLE NONE;SIDE SIDE VISIBLE NONE;SOURCE SOURCE VISIBLE NONE;STRUC STRUC VISIBLE NONE;SUBAREA SUBAREA VISIBLE NONE;TYPE TYPE VISIBLE NONE;CREATEDATE CREATEDATE VISIBLE NONE;UPDATEDATE UPDATEDATE VISIBLE NONE;IRIS_Road_Number IRIS_Road_Number VISIBLE NONE;LOwner LOwner VISIBLE NONE;ROwner ROwner VISIBLE NONE;LMaintainer LMaintainer VISIBLE NONE;RMaintainer RMaintainer VISIBLE NONE;BegPtFeature BegPtFeature VISIBLE NONE;EndPtFeature EndPtFeature VISIBLE NONE;Comments Comments VISIBLE NONE;ResearchHistory ResearchHistory VISIBLE NONE;Adjusted Adjusted VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;F_ZLEV F_ZLEV VISIBLE NONE;T_ZLEV T_ZLEV VISIBLE NONE;FFC FFC VISIBLE NONE;Shape Shape VISIBLE NONE")
    print("WashSt_2913 feature layer made")

    # Appends WashStr_2913 to RoadsAMS_ASSETS_Ops_WashCo_Roads
    arcpy.management.Append(inputs=[streets_WashStr_2913_vw_Laye],
                            target=RoadsAMS_ASSETS_Ops_WashCo_Roads,
                            schema_type="NO_TEST",
                            field_mapping="RoadNumber \"RoadNumber\" true true false 7 Text 0 0,First,#,streets_WashStr_2913_vw_Laye,IRIS_Road_Number,0,7;RoadName \"RoadName\" true true false 50 Text 0 0,First,#,streets_WashStr_2913_vw_Laye,FNAME,0,50;Location \"Location\" true true false 255 Text 0 0,First,#;CLASS \"RoadClassification\" true true false 2 Short 0 5,First,#,production.streets.WashStr_2913_vw,CLASS,-1,-1;URMD_Status \"URMD_Status\" true true false 2 Short 0 5,First,#;LOCALID \"LOCALID\" true true false 4 Long 0 10,First,#,production.streets.WashStr_2913_vw,LOCALID,-1,-1;Prefix \"Prefix\" true true false 5 Text 0 0,First,#,production.streets.WashStr_2913_vw,FDPRE,0,2;RoadType \"RoadType\" true true false 4 Text 0 0,First,#,production.streets.WashStr_2913_vw,FTYPE,0,4",
                            subtype="", expression="")

    print('WashStr_2913 streets appended to RoadsAMS_ASSETS_Ops_WashCo_Roads')

    # Calculates Cityworks AssetID's from WashStr_2913 LIDs
    arcpy.CalculateField_management(RoadsAMS_ASSETS_Ops_WashCo_Roads, 'AssetID', "'str-'+str(!LOCALID!)")

    # Calculates the URMD Status based on Functional Class field, URMD Boundary, and selection sets on PMSALL_Roads
    arcpy.MakeFeatureLayer_management(RoadsAMS_ASSETS_Ops_WashCo_Roads, 'URMD_FC', "CLASS IN (145, 151)")
    URMDFC_URMDarea = arcpy.SelectLayerByLocation_management('URMD_FC', 'INTERSECT', URMD_Area)
    arcpy.CalculateField_management(URMDFC_URMDarea, 'URMD_Status', '1')
    URMDFCFC_NotURMDarea = arcpy.SelectLayerByAttribute_management(URMDFC_URMDarea, 'SWITCH_SELECTION')
    arcpy.CalculateField_management(URMDFCFC_NotURMDarea, 'URMD_Status', '0')
    arcpy.MakeFeatureLayer_management(RoadsAMS_ASSETS_Ops_WashCo_Roads, 'NONURMD_FC', "CLASS NOT IN (145, 151)")
    arcpy.CalculateField_management('NONURMD_FC', 'URMD_Status', '0')

    # Calculates the location field
    arcpy.CalculateField_management(RoadsAMS_ASSETS_Ops_WashCo_Roads, 'Location',
                                    "!Prefix! + ' '  + !RoadName! + ' ' + !RoadType!")

    print("URMD Status calculated for RoadsAMS_ASSETS_Ops_WashCo_Roads")
    print('Done')

    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."

    Message = arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
    print(Message)

    Send(Title, Message, Error, EmailTo)

except:
    # sends email with errors
    Error = Error + 1
    Message = arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
    print (Message)

    Send(Title, Message, Error, EmailTo)
