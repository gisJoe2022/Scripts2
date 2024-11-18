# ---------------------------------------------------------------------------
# AddLoops.py
# Created on: 2011-07-11 14:56:25.00000
# Updated on: 2023-04-18 to support LRS revamp, deprecation of IRIS system, and python 3.7

# Description: Reprocesses problematic linear features using beg/end mileposting on every segment

# ---------------------------------------------------------------------------
import os, sys
cmd_folder = "\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy, smtplib, string

import gbl, trktime
from modEmail_3_7 import Send

Title = "Add Loops LRS Script"
Message = ""
Error = 0

# # Change to MyEmailRyan for dev
# EmailTo = gbl.MyEmailRyan
# !!!!Change back to GroupEmail when moving to Prod!!!.
EmailTo = gbl.GroupEmail

ScrptTimer = trktime.stopwatch()

arcpy.env.qualifiedFieldNames = False
# Local variables:
#***Source data***
NdSTREETS_WashStr = gbl.NdSTREETS+gbl.WashStr
NpSTREETS_lrs_LOOPS = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS.lrs_LOOPS"
NpSTREETS_CntyRouteCalib = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS.CntyRouteCalib"
RoadsAMS_Rds_ByRdName = gbl.RoadsAMS_Assets+"\\vw_AMSRoads"

#***Final Product***
NpSTREETS_LRS_Routes= "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreets.sde\\production.STREETS.LRS_Routes"
NdSTREETS_LRS_Routes = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NdStreets.sde\\distribution.STREETS.LRS_Routes"

#***Intermediate data***
NpSTREETSQC_lrs_LOOPS_prj = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.lrs_LOOPS_prj"
NpSTREETSQC_Lrs_loops_add_joined = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.Lrs_loops_add_joined"
NpSTREETSQC_lrs_LOOPS_add = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.lrs_LOOPS_add"

# global variables
WashStr_Layer = "WashStr_Layer"
BegMp = "BegMp"
EndMp = "EndMp"
WashStr_Layer1 = "WashStr_Layer1"
WashStr_Layer2 = "WashStr_Layer2"

try:
    # Process: Delete lrs_Loops_add_joined
    if arcpy.gp.exists(NpSTREETSQC_Lrs_loops_add_joined):
        arcpy.Delete_management(NpSTREETSQC_Lrs_loops_add_joined, "FeatureClass")

    # Process: Delete lrs_Loops_add
    if arcpy.gp.exists(NpSTREETSQC_lrs_LOOPS_add):
        arcpy.Delete_management(NpSTREETSQC_lrs_LOOPS_add, "FeatureClass")

    # Process: Clear Workspace Cache
    arcpy.ClearWorkspaceCache_management("")

    # Process: Make WashStr Feature Layer
    arcpy.MakeFeatureLayer_management(NdSTREETS_WashStr, WashStr_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;LOCALID LOCALID VISIBLE NONE;LEFTADD1 LEFTADD1 VISIBLE NONE;LEFTADD2 LEFTADD2 VISIBLE NONE;RGTADD1 RGTADD1 VISIBLE NONE;RGTADD2 RGTADD2 VISIBLE NONE;FDPRE FDPRE VISIBLE NONE;FNAME FNAME VISIBLE NONE;FTYPE FTYPE VISIBLE NONE;FDSUF FDSUF VISIBLE NONE;LZIP LZIP VISIBLE NONE;RZIP RZIP VISIBLE NONE;LCITY LCITY VISIBLE NONE;RCITY RCITY VISIBLE NONE;LCOUNTY LCOUNTY VISIBLE NONE;RCOUNTY RCOUNTY VISIBLE NONE;CFCC CFCC VISIBLE NONE;CLASS CLASS VISIBLE NONE;DRCT DRCT VISIBLE NONE;LEADZERO LEADZERO VISIBLE NONE;QUIRK QUIRK VISIBLE NONE;SIDE SIDE VISIBLE NONE;SOURCE SOURCE VISIBLE NONE;STRUC STRUC VISIBLE NONE;SUBAREA SUBAREA VISIBLE NONE;TYPE TYPE VISIBLE NONE;CREATEDATE CREATEDATE VISIBLE NONE;UPDATEDATE UPDATEDATE VISIBLE NONE;Alias Alias VISIBLE NONE;IRIS_Road_Number IRIS_Road_Number VISIBLE NONE;LOwner LOwner VISIBLE NONE;ROwner ROwner VISIBLE NONE;LMaintainer LMaintainer VISIBLE NONE;RMaintainer RMaintainer VISIBLE NONE;Other_Jur_Asset_Number Other_Jur_Asset_Number VISIBLE NONE;BegPtFeature BegPtFeature VISIBLE NONE;EndPtFeature EndPtFeature VISIBLE NONE;Comments Comments VISIBLE NONE;QC QC VISIBLE NONE;XY_Source XY_Source VISIBLE NONE;ResearchHistory ResearchHistory VISIBLE NONE;XY_CHK XY_CHK VISIBLE NONE;Attribute_CHK Attribute_CHK VISIBLE NONE;MSAG_CHK MSAG_CHK VISIBLE NONE;Adjusted Adjusted VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;F_ZLEV F_ZLEV VISIBLE NONE;T_ZLEV TZLEV VISIBLE NONE;Shape Shape VISIBLE NONE;Shape.len Shape.len VISIBLE NONE")

    # Process: Add Join to Loops table
    arcpy.AddJoin_management(WashStr_Layer, "IRIS_Road_Number", NpSTREETS_lrs_LOOPS, "IRIS_Road_Number", "KEEP_ALL")

    # Process: Select Layer By Loops
    arcpy.SelectLayerByAttribute_management(WashStr_Layer, "NEW_SELECTION", "production.STREETS.lrs_LOOPS.IRIS_Road_Number IS NOT NULL")

    # Process: Remove Join to Loops table
    arcpy.RemoveJoin_management(WashStr_Layer, "#")

    # Process: Make Query Table of Begin Calibration points
    arcpy.MakeQueryTable_management(NpSTREETS_CntyRouteCalib, BegMp,
                                    "USE_KEY_FIELDS", "", "CntyRouteCalib.LOCALID #;CntyRouteCalib.IRIS_Road_Number #;CntyRouteCalib.MilePost #;CntyRouteCalib.LIDPct #", "LIDPct = 0")
    print ("Loops found")
    # Process: Add Join to WashStr
    arcpy.AddJoin_management(WashStr_Layer, "LOCALID", BegMp, "CntyRouteCalib.LOCALID", "KEEP_ALL")
    print ("BegMP join completed")

    # Process: Make Query Table of End Calibration points
    arcpy.management.MakeQueryTable(in_table=[NpSTREETS_CntyRouteCalib], out_table=EndMp,
                                    in_key_field_option="USE_KEY_FIELDS", in_key_field=[],
                                    in_field=[["Production.STREETS.CntyRouteCalib.LOCALID", ""],
                                              ["Production.STREETS.CntyRouteCalib.IRIS_Road_Number", ""],
                                              ["Production.STREETS.CntyRouteCalib.MilePost", ""]],
                                    where_clause="Production.STREETS.CntyRouteCalib.LIDPct = 100")

    # Process: Make Feature Layer of WashStr with End points
    arcpy.management.MakeFeatureLayer(WashStr_Layer, WashStr_Layer1,"","",
                                      "distribution.STREETS.WashStr.OBJECTID distribution.STREETS.WashStr.OBJECTID VISIBLE NONE;distribution.STREETS.WashStr.LOCALID distribution.STREETS.WashStr.LOCALID VISIBLE NONE;distribution.STREETS.WashStr.LEFTADD1 distribution.STREETS.WashStr.LEFTADD1 VISIBLE NONE;distribution.STREETS.WashStr.LEFTADD2 distribution.STREETS.WashStr.LEFTADD2 VISIBLE NONE;distribution.STREETS.WashStr.RGTADD1 distribution.STREETS.WashStr.RGTADD1 VISIBLE NONE;distribution.STREETS.WashStr.RGTADD2 distribution.STREETS.WashStr.RGTADD2 VISIBLE NONE;distribution.STREETS.WashStr.FDPRE distribution.STREETS.WashStr.FDPRE VISIBLE NONE;distribution.STREETS.WashStr.FNAME distribution.STREETS.WashStr.FNAME VISIBLE NONE;distribution.STREETS.WashStr.FTYPE distribution.STREETS.WashStr.FTYPE VISIBLE NONE;distribution.STREETS.WashStr.FDSUF distribution.STREETS.WashStr.FDSUF VISIBLE NONE;distribution.STREETS.WashStr.LZIP distribution.STREETS.WashStr.LZIP VISIBLE NONE;distribution.STREETS.WashStr.RZIP distribution.STREETS.WashStr.RZIP VISIBLE NONE;distribution.STREETS.WashStr.LCITY distribution.STREETS.WashStr.LCITY VISIBLE NONE;distribution.STREETS.WashStr.RCITY distribution.STREETS.WashStr.RCITY VISIBLE NONE;distribution.STREETS.WashStr.LCOUNTY distribution.STREETS.WashStr.LCOUNTY VISIBLE NONE;distribution.STREETS.WashStr.RCOUNTY distribution.STREETS.WashStr.RCOUNTY VISIBLE NONE;distribution.STREETS.WashStr.CFCC distribution.STREETS.WashStr.CFCC VISIBLE NONE;distribution.STREETS.WashStr.CLASS distribution.STREETS.WashStr.CLASS VISIBLE NONE;distribution.STREETS.WashStr.DRCT distribution.STREETS.WashStr.DRCT VISIBLE NONE;distribution.STREETS.WashStr.LEADZERO distribution.STREETS.WashStr.LEADZERO VISIBLE NONE;distribution.STREETS.WashStr.QUIRK distribution.STREETS.WashStr.QUIRK VISIBLE NONE;distribution.STREETS.WashStr.SIDE distribution.STREETS.WashStr.SIDE VISIBLE NONE;distribution.STREETS.WashStr.SOURCE distribution.STREETS.WashStr.SOURCE VISIBLE NONE;distribution.STREETS.WashStr.STRUC distribution.STREETS.WashStr.STRUC VISIBLE NONE;distribution.STREETS.WashStr.SUBAREA distribution.STREETS.WashStr.SUBAREA VISIBLE NONE;distribution.STREETS.WashStr.TYPE distribution.STREETS.WashStr.TYPE VISIBLE NONE;distribution.STREETS.WashStr.CREATEDATE distribution.STREETS.WashStr.CREATEDATE VISIBLE NONE;distribution.STREETS.WashStr.UPDATEDATE distribution.STREETS.WashStr.UPDATEDATE VISIBLE NONE;distribution.STREETS.WashStr.Alias distribution.STREETS.WashStr.Alias VISIBLE NONE;distribution.STREETS.WashStr.IRIS_Road_Number distribution.STREETS.WashStr.IRIS_Road_Number VISIBLE NONE;distribution.STREETS.WashStr.LOwner distribution.STREETS.WashStr.LOwner VISIBLE NONE;distribution.STREETS.WashStr.ROwner distribution.STREETS.WashStr.ROwner VISIBLE NONE;distribution.STREETS.WashStr.LMaintainer distribution.STREETS.WashStr.LMaintainer VISIBLE NONE;distribution.STREETS.WashStr.RMaintainer distribution.STREETS.WashStr.RMaintainer VISIBLE NONE;distribution.STREETS.WashStr.Other_Jur_Asset_Number distribution.STREETS.WashStr.Other_Jur_Asset_Number VISIBLE NONE;distribution.STREETS.WashStr.BegPtFeature distribution.STREETS.WashStr.BegPtFeature VISIBLE NONE;distribution.STREETS.WashStr.EndPtFeature distribution.STREETS.WashStr.EndPtFeature VISIBLE NONE;distribution.STREETS.WashStr.Comments distribution.STREETS.WashStr.Comments VISIBLE NONE;distribution.STREETS.WashStr.QC distribution.STREETS.WashStr.QC VISIBLE NONE;distribution.STREETS.WashStr.XY_Source distribution.STREETS.WashStr.XY_Source VISIBLE NONE;distribution.STREETS.WashStr.ResearchHistory distribution.STREETS.WashStr.ResearchHistory VISIBLE NONE;distribution.STREETS.WashStr.XY_CHK distribution.STREETS.WashStr.XY_CHK VISIBLE NONE;distribution.STREETS.WashStr.Attribute_CHK distribution.STREETS.WashStr.Attribute_CHK VISIBLE NONE;distribution.STREETS.WashStr.MSAG_CHK distribution.STREETS.WashStr.MSAG_CHK VISIBLE NONE;distribution.STREETS.WashStr.Adjusted distribution.STREETS.WashStr.Adjusted VISIBLE NONE;distribution.STREETS.WashStr.GlobalID distribution.STREETS.WashStr.GlobalID VISIBLE NONE;distribution.STREETS.WashStr.F_ZLEV distribution.STREETS.WashStr.F_ZLEV VISIBLE NONE;distribution.STREETS.WashStr.T_ZLEV distribution.STREETS.WashStr.T_ZLEV VISIBLE NONE;distribution.STREETS.WashStr.FFC distribution.STREETS.WashStr.FFC VISIBLE NONE;Shape Shape VISIBLE NONE;distribution.STREETS.WashStr.BufDist distribution.STREETS.WashStr.BufDist VISIBLE NONE;Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_LOCALID Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_LOCALID VISIBLE NONE;Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_IRIS_Road_Number Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_IRIS_Road_Number VISIBLE NONE;Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_MilePost Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_MilePost VISIBLE NONE")
    # Process: Add Join to Washstr
    arcpy.management.AddJoin(WashStr_Layer1, "distribution.STREETS.WashStr.LOCALID",EndMp, "Production.STREETS.CntyRouteCalib.LOCALID")
    print("EndMP join completed")

    # Make Feature Layer of joined data for copy features
    arcpy.MakeFeatureLayer_management(WashStr_Layer1, WashStr_Layer2,"", "",
                                      "distribution.STREETS.WashStr.OBJECTID distribution.STREETS.WashStr.OBJECTID VISIBLE NONE;distribution.STREETS.WashStr.LOCALID distribution.STREETS.WashStr.LOCALID VISIBLE NONE;distribution.STREETS.WashStr.LEFTADD1 distribution.STREETS.WashStr.LEFTADD1 VISIBLE NONE;distribution.STREETS.WashStr.LEFTADD2 distribution.STREETS.WashStr.LEFTADD2 VISIBLE NONE;distribution.STREETS.WashStr.RGTADD1 distribution.STREETS.WashStr.RGTADD1 VISIBLE NONE;distribution.STREETS.WashStr.RGTADD2 distribution.STREETS.WashStr.RGTADD2 VISIBLE NONE;distribution.STREETS.WashStr.FDPRE distribution.STREETS.WashStr.FDPRE VISIBLE NONE;distribution.STREETS.WashStr.FNAME distribution.STREETS.WashStr.FNAME VISIBLE NONE;distribution.STREETS.WashStr.FTYPE distribution.STREETS.WashStr.FTYPE VISIBLE NONE;distribution.STREETS.WashStr.FDSUF distribution.STREETS.WashStr.FDSUF VISIBLE NONE;distribution.STREETS.WashStr.LZIP distribution.STREETS.WashStr.LZIP VISIBLE NONE;distribution.STREETS.WashStr.RZIP distribution.STREETS.WashStr.RZIP VISIBLE NONE;distribution.STREETS.WashStr.LCITY distribution.STREETS.WashStr.LCITY VISIBLE NONE;distribution.STREETS.WashStr.RCITY distribution.STREETS.WashStr.RCITY VISIBLE NONE;distribution.STREETS.WashStr.LCOUNTY distribution.STREETS.WashStr.LCOUNTY VISIBLE NONE;distribution.STREETS.WashStr.RCOUNTY distribution.STREETS.WashStr.RCOUNTY VISIBLE NONE;distribution.STREETS.WashStr.CFCC distribution.STREETS.WashStr.CFCC VISIBLE NONE;distribution.STREETS.WashStr.CLASS distribution.STREETS.WashStr.CLASS VISIBLE NONE;distribution.STREETS.WashStr.DRCT distribution.STREETS.WashStr.DRCT VISIBLE NONE;distribution.STREETS.WashStr.LEADZERO distribution.STREETS.WashStr.LEADZERO VISIBLE NONE;distribution.STREETS.WashStr.QUIRK distribution.STREETS.WashStr.QUIRK VISIBLE NONE;distribution.STREETS.WashStr.SIDE distribution.STREETS.WashStr.SIDE VISIBLE NONE;distribution.STREETS.WashStr.SOURCE distribution.STREETS.WashStr.SOURCE VISIBLE NONE;distribution.STREETS.WashStr.STRUC distribution.STREETS.WashStr.STRUC VISIBLE NONE;distribution.STREETS.WashStr.SUBAREA distribution.STREETS.WashStr.SUBAREA VISIBLE NONE;distribution.STREETS.WashStr.TYPE distribution.STREETS.WashStr.TYPE VISIBLE NONE;distribution.STREETS.WashStr.CREATEDATE distribution.STREETS.WashStr.CREATEDATE VISIBLE NONE;distribution.STREETS.WashStr.UPDATEDATE distribution.STREETS.WashStr.UPDATEDATE VISIBLE NONE;distribution.STREETS.WashStr.Alias distribution.STREETS.WashStr.Alias VISIBLE NONE;distribution.STREETS.WashStr.IRIS_Road_Number distribution.STREETS.WashStr.IRIS_Road_Number VISIBLE NONE;distribution.STREETS.WashStr.LOwner distribution.STREETS.WashStr.LOwner VISIBLE NONE;distribution.STREETS.WashStr.ROwner distribution.STREETS.WashStr.ROwner VISIBLE NONE;distribution.STREETS.WashStr.LMaintainer distribution.STREETS.WashStr.LMaintainer VISIBLE NONE;distribution.STREETS.WashStr.RMaintainer distribution.STREETS.WashStr.RMaintainer VISIBLE NONE;distribution.STREETS.WashStr.Other_Jur_Asset_Number distribution.STREETS.WashStr.Other_Jur_Asset_Number VISIBLE NONE;distribution.STREETS.WashStr.BegPtFeature distribution.STREETS.WashStr.BegPtFeature VISIBLE NONE;distribution.STREETS.WashStr.EndPtFeature distribution.STREETS.WashStr.EndPtFeature VISIBLE NONE;distribution.STREETS.WashStr.Comments distribution.STREETS.WashStr.Comments VISIBLE NONE;distribution.STREETS.WashStr.QC distribution.STREETS.WashStr.QC VISIBLE NONE;distribution.STREETS.WashStr.XY_Source distribution.STREETS.WashStr.XY_Source VISIBLE NONE;distribution.STREETS.WashStr.ResearchHistory distribution.STREETS.WashStr.ResearchHistory VISIBLE NONE;distribution.STREETS.WashStr.XY_CHK distribution.STREETS.WashStr.XY_CHK VISIBLE NONE;distribution.STREETS.WashStr.Attribute_CHK distribution.STREETS.WashStr.Attribute_CHK VISIBLE NONE;distribution.STREETS.WashStr.MSAG_CHK distribution.STREETS.WashStr.MSAG_CHK VISIBLE NONE;distribution.STREETS.WashStr.Adjusted distribution.STREETS.WashStr.Adjusted VISIBLE NONE;distribution.STREETS.WashStr.GlobalID distribution.STREETS.WashStr.GlobalID VISIBLE NONE;distribution.STREETS.WashStr.F_ZLEV distribution.STREETS.WashStr.F_ZLEV VISIBLE NONE;distribution.STREETS.WashStr.T_ZLEV distribution.STREETS.WashStr.T_ZLEV VISIBLE NONE;distribution.STREETS.WashStr.FFC distribution.STREETS.WashStr.FFC VISIBLE NONE;distribution.STREETS.WashStr.Shape distribution.STREETS.WashStr.Shape VISIBLE NONE;distribution.STREETS.WashStr.BufDist distribution.STREETS.WashStr.BufDist VISIBLE NONE;Shape.STLength() Shape.STLength() VISIBLE NONE;Production.STREETS.CntyRouteCalib.LOCALID Production.STREETS.CntyRouteCalib.LOCALID VISIBLE NONE;Production.STREETS.CntyRouteCalib.IRIS_Road_Number Production.STREETS.CntyRouteCalib.IRIS_Road_Number VISIBLE NONE;Production.STREETS.CntyRouteCalib.MilePost Production.STREETS.CntyRouteCalib.MilePost VISIBLE NONE;Production.STREETS.CntyRouteCalib.LOCALID Production.STREETS.CntyRouteCalib.LOCALID VISIBLE NONE;Production.STREETS.CntyRouteCalib.IRIS_Road_Number Production.STREETS.CntyRouteCalib.IRIS_Road_Number VISIBLE NONE;Production.STREETS.CntyRouteCalib.MilePost Production.STREETS.CntyRouteCalib.MilePost VISIBLE NONE;distribution.STREETS.WashStr.MilePost distribution.STREETS.WashStr.MilePost VISIBLE NONE;distribution.STREETS.WashStr.Production_STREETS_CntyRouteCalib_LOCALID distribution.STREETS.WashStr.Production_STREETS_CntyRouteCalib_LOCALID VISIBLE NONE;distribution.STREETS.WashStr.Production_STREETS_CntyRouteCalib_IRIS_Road_Number distribution.STREETS.WashStr.Production_STREETS_CntyRouteCalib_IRIS_Road_Number VISIBLE NONE;distribution.STREETS.WashStr.Production_STREETS_CntyRouteCalib_MilePost distribution.STREETS.WashStr.Production_STREETS_CntyRouteCalib_MilePost VISIBLE NONE;Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_LOCALID Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_LOCALID VISIBLE NONE;Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_IRIS_Road_Number Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_IRIS_Road_Number VISIBLE NONE;Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_MilePost Production.STREETS.EndMp.Production_STREETS_CntyRouteCalib_MilePost VISIBLE NONE")
    # Process: Copy Features of Joined data
    arcpy.CopyFeatures_management(WashStr_Layer2, NpSTREETSQC_Lrs_loops_add_joined, "", "0", "0", "0")

    # Process: Delete Features in NpSTREETSQC_lrs_LOOPS_prj
    arcpy.DeleteFeatures_management(NpSTREETSQC_lrs_LOOPS_prj)
    # Process: Append data to correctly projected schema NpSTREETSQC_lrs_LOOPS_prj
    # ***** To Do: database connection in field mapping needs to be changed to global if possible
    arcpy.management.Append(NpSTREETSQC_Lrs_loops_add_joined, NpSTREETSQC_lrs_LOOPS_prj, "NO_TEST",
                            "IRIS_Road_Number \"IRIS_Road_Number\" true true false 10 Text 0 0,First,#,\\\\emcgis\\NAS\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.Lrs_loops_add_joined,IRIS_Road_Number,0,7;Milepost \"Milepost\" true true false 8 Double 3 18,First,#,\\\\emcgis\\NAS\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.Lrs_loops_add_joined,MilePost,-1,-1;Milepost_1 \"Milepost_1\" true true false 8 Double 3 18,First,#,\\\\emcgis\\NAS\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS_QC.Lrs_loops_add_joined,MilePost_1,-1,-1",
                            subtype="", expression="")
    print ("Added begin and end milepost fields")

    # Process: Create Routes
    arcpy.CreateRoutes_lr(NpSTREETSQC_lrs_LOOPS_prj, "IRIS_Road_Number", NpSTREETSQC_lrs_LOOPS_add, "TWO_FIELDS", "MilePost", "MilePost_1", "LOWER_RIGHT", "1", "0", "IGNORE", "INDEX")
    print ("Routes created")

    # Process: Append (2)
    # ***** To Do: database connection in field mapping needs to be changed to global if possible
    # arcpy.management.Append(inputs=[NpSTREETSQC_lrs_LOOPS_add], target=NpSTREETS_LRS_Routes,
    #                         schema_type="NO_TEST",
    #                         field_mapping="IRIS_Road_Number \"IRIS_Road_Number\" true true false 8 Text 0 0,First,#,\\\\emcgis\\NAS\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\NpStreetsQC.sde\\production.STREETS.lrs_LOOPS_add,IRIS_Road_Number,0,10;Identifier \"ID\" true true false 4 Long 0 10,First,#",
    #                         subtype="", expression="")
    arcpy.management.Append(NpSTREETSQC_lrs_LOOPS_add, NpSTREETS_LRS_Routes, "NO_TEST",
                            r'IRIS_Road_Number "IRIS_Road_Number" true true false 8 Text 0 0,First,#,\\emcgis\NAS\LUTOPS\GIS\Admin\ArcCatalog\ArcpySDEdbConnections\NpStreetsQC.sde\production.STREETS_QC.lrs_LOOPS_add,IRIS_Road_Number,0,10;Identifier "ID" true true false 4 Long 0 10,First,#',
                            '', '')

    print ("Appended routes")

    # Add road name and milepost fields
    arcpy.AddField_management(NpSTREETS_LRS_Routes, "Road_Name", "TEXT", "", "", 50)
    arcpy.AddField_management(NpSTREETS_LRS_Routes, "Milepost_Begin", "DOUBLE", 38, 8)
    arcpy.AddField_management(NpSTREETS_LRS_Routes, "Milepost_End", "DOUBLE", 38, 8)

    # Calculate road name and mileposts fields based on join with Roads AMS Road Name view
    arcpy.MakeFeatureLayer_management(NpSTREETS_LRS_Routes, "lyr_lrs_IRIS_Routes")
    arcpy.AddJoin_management("lyr_" + gbl.lrs_IRIS_Routes, "IRIS_Road_Number", RoadsAMS_Rds_ByRdName, "Road_Number")
    arcpy.CalculateField_management("lyr_" + gbl.lrs_IRIS_Routes, "Road_Name",
                                    "!RoadsAMS.Assets.vw_AMSRoads.Road_Name! + ' ' + !RoadsAMS.Assets.vw_AMSRoads.road_type!", "PYTHON_9.3")
    arcpy.CalculateField_management("lyr_" + gbl.lrs_IRIS_Routes, "Milepost_Begin",
                                    "!RoadsAMS.Assets.vw_AMSRoads.Beg_Milepost!", "PYTHON_9.3")
    arcpy.CalculateField_management("lyr_" + gbl.lrs_IRIS_Routes, "Milepost_End",
                                    "!RoadsAMS.Assets.vw_AMSRoads.End_Milepost!", "PYTHON_9.3")
    print("Finished calculating road name and milepost fields")

    # Updates LRS_Routes on nutsde.distro
    arcpy.TruncateTable_management(NdSTREETS_LRS_Routes)
    # Process: Append (3)
    arcpy.Append_management(NpSTREETS_LRS_Routes, NdSTREETS_LRS_Routes, "NO_TEST", "", "")
    print ("New routes posted")
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