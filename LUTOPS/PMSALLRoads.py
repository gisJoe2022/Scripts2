# ---------------------------------------------------------------------------
# PMSALLRoads.py
# Created on: 2011-09-12 14:05:45.00000
# Updated on: 2022-12-07 for Cityworks integration and RoadsAMS_Assets geodatabase and python 3.7

# Description: Creates a pavement road system (PMS) using linear referencing and a query on RoadNet to RoadsAMS_Assets and the production and distribution databases on Nutsde.
# ArcGIS software (licensing ArcEditor or higher), Nutsde & SQL1 servers, and appropriate permissions are required to run this script.
# ---------------------------------------------------------------------------

#Allows importing of custom modules
import os, sys
cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy
arcpy.env.workspace = r"\\pwebgisapp1\GIS_Process_Scripts\ConnectionFiles\nutsde_roadsams_ASSETS.sde"
arcpy.env.overwriteOutput = True

# Import custom modules
import gbl, trktime
from DataTransfer.modMoveData_3_7 import GISDelete, GISCopy, GISDeleteFeatures, GISAppendFeatures, GISTruncate
from DataTransfer.mod_lin_ref_IRIS_3_7 import IRIS_lin_ref
from modEmail_3_7 import Send

# Input Datasets
NdTRANSPOR_PMSAll_Roads = gbl.NdTRANSPOR+gbl.PMSAll_Roads
# RoadsAMS_PMSALL_Roads = gbl.RoadsAMS_Assets+"\\Ops_PMSAll_Roads"
RoadsAMS_PMSALL_Roads = gbl.RoadsAMS_Assets+"\\Ops_PMSALL_Roads"
URMD_Area = gbl.RoadsAMS_Assets+"\\URMD_Area"
#!!!Liner referencing data source that will need to be switched out when new LRS scripts are ready for prod!!!
LRS_Routes = gbl.NdSTREETS+gbl.LRS_Routes
LID_Routes = gbl.NdSTREETS+gbl.LID_Routes

# Output Datasets
PMSALLRoads_Project2913 = gbl.NpTRANSPOR+'PMSAll_Roads_Project2913_Staging'
PMSAllRoads_Convert_WashStr = gbl.NpTRANSPOR+gbl.PMSAllRoads_Convert_WashStr
NpTRANSPOR_WC_Pavement = gbl.NpTRANSPOR+gbl.WC_Pavement
WBUG_WC_Pavement = gbl.WBUG_TRANSPOR+gbl.WC_Pavement

Title = "PMS All Roads log"
Message = ""
Error = 0

# # Change to MyEmailRyan for dev
# EmailTo = gbl.MyEmailRyan
# !!!!Change back to GroupEmail when moving to Prod!!!.
EmailTo = gbl.GroupEmail

ScrptTimer = trktime.stopwatch()

try:

# Process: Clear Workspace Cache
    arcpy.ClearWorkspaceCache_management("")
    if arcpy.Exists(gbl.RdNet + gbl.vw_PMS_All_Roads):
        if int(arcpy.GetCount_management(gbl.RdNet + gbl.vw_PMS_All_Roads).getOutput(0))>0:
            # Deletes all features from RoadsAMS.PMSALL_Roads
            Temp = GISDeleteFeatures(NdTRANSPOR_PMSAll_Roads)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail
            print("NdTRANSPOR_PMSAll_Roads features deleted")

        # Create PMSAll_Roads Routes
            pmstemp = IRIS_lin_ref("LINE", gbl.RdNet, gbl.vw_PMS_All_Roads, "Road_Number", "Beg_MP", "End_MP", "","")
            pmsLines = pmstemp.line
            Message = Message + pmstemp.msg.appendMessage
            Error = Error + pmstemp.msg.fail
            print ("Pavement Management Routes Created")

        # Appends Route Features to RoadsAMS.PMSALL_Roads
            arcpy.MakeFeatureLayer_management(pmsLines, 'PMSAllRoads_LR')
            # arcpy.management.Append('PMSAllRoads_LR', RoadsAMS_PMSAll_Roads, schema_type="NO_TEST", field_mapping="RoadSectionID \"RoadSectionID\" true false false 21 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,RoadSectionID,0,21;Road_Number \"Road_Number\" true false false 10 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Road_Number,0,10;Sec_ID \"Sec_ID\" true false false 10 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Sec_ID,0,10;Road_Name \"Road_Name\" true true false 30 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Road_Name,0,30;Beg_MP \"Beg_MP\" true true false 4 Float 3 6,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Beg_MP,-1,-1;Beg_Loc \"Beg_Loc\" true false false 100 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Beg_Loc,0,100;End_MP \"End_MP\" true true false 4 Float 3 6,First,#,\\\\emcgis\\NAS\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\SQL1_RoadNet.sde\\RoadNet.dbo.vw_PMS_All_Roads_Features,End_MP,-1,-1;End_Loc \"End_Loc\" true false false 100 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,End_Loc,0,100;Beg_Ft \"Beg_Ft\" true true false 8 Double 8 38,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Beg_Ft,-1,-1;End_Ft \"End_Ft\" true true false 8 Double 8 38,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,End_Ft,-1,-1;Sec_Len_Ft \"Sec_Len_Ft\" true false false 8 Double 8 38,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Sec_Len_Ft,-1,-1;FC \"FC\" true true false 50 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,FC,0,50;PCI \"PCI\" true false false 4 Long 0 10,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,PCI,-1,-1;Lanes \"Lanes\" true false false 2 Short 0 5,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Lanes,-1,-1;Width_Rd \"Width_Rd\" true false false 4 Float 2 6,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Width_Rd,-1,-1;Surf_Type \"Surf_Type\" true true false 50 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Surf_Type,0,50;Section_Key \"Section_Key\" true false false 10 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,Section_Key,0,10;lastMaintenanceDate \"lastMaintenanceDate\" true false false 8 Date 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,lastMaintenanceDate,-1,-1;lastMaintenanceCalendarYear \"lastMaintenanceCalendarYear\" true true false 4 Long 0 10,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,lastMaintenanceCalendarYear,-1,-1;lastTreatmentType \"lastTreatmentType\" true false false 50 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,lastTreatmentType,0,50;maintenanceHistory_key \"maintenanceHistory_key\" true true false 10 Text 0 0,First,#,gbl.RdNet + gbl.vw_PMS_All_Roads,maintenanceHistory_key,0,10;URMD_Status \"URMD_Status\" true true false 2 Short 0 5,First,#", subtype="", expression="")
            Temp = GISAppendFeatures('PMSAllRoads_LR', NdTRANSPOR_PMSAll_Roads)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail
            print ("Pavement Management routes appended to NdTRANSPOR_PMSAll_Roads")

         # Reprojects NdTRANSPOR_PMSAll_Roads to staging FC also on Production
            arcpy.Project_management(NdTRANSPOR_PMSAll_Roads,
                                 PMSALLRoads_Project2913,
                                 "PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',8202099.737532808],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Foot',0.3048]]",
                                 transform_method=[],
                                 in_coor_system="PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1553.424873737374],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Mile_US',1609.347218694438]]",
                                 preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
            print("NdTRANSPOR_PMSAll_Roads reprojected to 2913")

         # Deletes all features from RoadsAMS.PMSALL_Roads
            Temp = GISDeleteFeatures(RoadsAMS_PMSALL_Roads)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail
            print("RoadsAMS_PMSALL_Roads features deleted")

         #  Appends features to RoadsAMS_PMSALL_Roads
            print("Append features to RoadsAMS")
            Temp = GISAppendFeatures(PMSALLRoads_Project2913, RoadsAMS_PMSALL_Roads)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail
            print("Pavement Management routes appended to RoadsAMS.PMSALL_Roads")

        # Populates Cityworks AssetID field with StreetSaver section ID
            arcpy.management.CalculateField(RoadsAMS_PMSALL_Roads, "AssetID", "!RoadSectionID!", "PYTHON3")
        # Populates Cityworks Location field with StreetSaver Road Name and From and To cross streets.
            arcpy.CalculateField_management(RoadsAMS_PMSALL_Roads,'Location', "!Road_Name! + ' - ' + !Beg_Loc! + ' to ' +  !End_Loc!", 'PYTHON3')
        # Calculates the URMD Status based on Functional Class field, URMD Boundary, and selection sets on PMSALL_Roads
            arcpy.MakeFeatureLayer_management(RoadsAMS_PMSALL_Roads,'URMD_FC',"FC IN ('UL','NR')")
            URMDFC_URMDarea = arcpy.SelectLayerByLocation_management ('URMD_FC','INTERSECT', URMD_Area)
            arcpy.CalculateField_management(URMDFC_URMDarea,'URMD_Status','1')
            URMDFCFC_NotURMDarea = arcpy.SelectLayerByAttribute_management(URMDFC_URMDarea,'SWITCH_SELECTION')
            arcpy.CalculateField_management(URMDFCFC_NotURMDarea, 'URMD_Status', '0', 'PYTHON3')
            arcpy.MakeFeatureLayer_management(RoadsAMS_PMSALL_Roads, 'NONURMD_FC', "FC NOT IN ('UL','NR')")
            arcpy.CalculateField_management('NONURMD_FC', 'URMD_Status', '0', 'PYTHON3')
            print ("Asset ID, Location, and URMD Status calculated for RoadsAMS_PMSALL_Roads")

        # Creates and updates WC_Pavement for GISBUG
        # Deletes production.TRANSPOR.PMSAllRoads_Convert_WashStr
            print ("Delete production.PMSAllRoads_Convert_WashStr")
            Temp = GISDelete(PMSAllRoads_Convert_WashStr)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail

            #Transform back to WashStr
            print ("Transform back to WashStr")
            arcpy.TransformRouteEvents_lr(NdTRANSPOR_PMSAll_Roads,"Road_Number LINE Beg_MP End_MP",LRS_Routes,"IRIS_Road_Number",LID_Routes,"LOCALID",PMSAllRoads_Convert_WashStr,"LOCALID LINE Beg_PER_Line End_PER_Line","15 Feet","FIELDS")

            # !!!!!!Uses liner referencing data sources that will need to be switched out when ready for Prod!!!!
            print ("Make Route Event Layer")
            arcpy.MakeRouteEventLayer_lr(LID_Routes,"LOCALID",PMSAllRoads_Convert_WashStr,"LOCALID LINE Beg_PER_Line End_PER_Line","pmsWashstr","#","NO_ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")

            # Deletes production.TRANSPOR.WC_Pavement
            print ("Delete production.WC_Pavement")
            Temp = GISDelete(NpTRANSPOR_WC_Pavement)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail

            # Copy WC_Pavement Features
            print ("Copy Pavement Management routes to production")
            Temp = GISCopy("pmsWashstr", NpTRANSPOR_WC_Pavement)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail

        # Deletes features from GISBUG.TRANSPOR.Pavement
            print ("Delete features from distribution")
            Temp = GISTruncate(WBUG_WC_Pavement)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail

        # Appends features to GISBUG.TRANSPOR.WC_Pavement
            print ("Append features to distribution")
            Temp = GISAppendFeatures(NpTRANSPOR_WC_Pavement, WBUG_WC_Pavement)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail

        else:
            Error=Error+1
            Message= Message + "\n" + 'No features exist. Update aborted.'
            raise NameError('No features exist')

    else:
        Error=Error+1
        Message= Message + "\n" + 'Source table does not exist. Update aborted.'
        raise NameError('Source table does not exist')

#Adds a final script time to email
    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."

    print ("All Done!!!")

# Send email with successful operations
    Send(Title, Message, Error, EmailTo)

except:  #send email with errors

    Error = Error + 1
    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
    print(Message)
    Send(Title, Message, Error, EmailTo)