# Creates linear referencing route event for point, line, and both situations.  Created in 10.0.1

import os, sys
#cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import arcpy
from arcpy import env
import gbl, trktime

class lrs:
    msg = gbl.PassMessage()
    point=""
    line =""
linref = lrs()

env.qualifiedFieldNames = False
env.overwriteOutput = True
env.workspace = "in_memory"

# Set the MResolution
arcpy.env.MResolution = 0.00005

# Set the MDomain
arcpy.env.MDomain = "-100 10000000"


def IRIS_lin_ref(

lrType,         #Defines type of linear referencing; "POINT", "LINE", or "BOTH"
dataConnect,    #First part of linear referenced database path
tblName,        #Table to be linear referenced
RdNumFld,       #Linear referenced ID field (i.e. IRIS_Road_Number)
BegMp,          #Begin milepost
EndMp,          #End milepost, "" if POINT
SQLqry,         #Simple SQL query to restrict table, "" if not needed
OffSet):        #Offset distance field, "" if not needed

    linref = lrs()
##    linref.point=tblName[:6]
##    linref.point="lyr"+linref.point+"pts"
    linref.point="lyr"+tblName[:3]+"pts"
    print (linref.point)
    linref.line ="lyr"+tblName[:3]+"lines"
    BeginTime = trktime.stopwatch()

    intbl = "qrytbl"+tblName[:3]+lrType[:1]

    if lrType=="POINT":         # Processes routed event layer for point data
        try:

            if dataConnect.find(".odc")!=-1:
                if tblName !="":
                    arcpy.MakeQueryTable_management(dataConnect+tblName, intbl, "ADD_VIRTUAL_KEY_FIELD", "", "", SQLqry)
                else:
                    arcpy.MakeQueryTable_management(dataConnect, intbl, "ADD_VIRTUAL_KEY_FIELD", "", "", SQLqry)

            else:
                if tblName !="":
                    if SQLqry !="":
                        arcpy.MakeTableView_management(dataConnect+tblName, intbl, SQLqry)

                    else:
                        intbl = dataConnect+tblName
                else:
                    if SQLqry!="":
                        arcpy.MakeTableView_management(dataConnect, intbl, SQLqry)
                    else:
                        intbl = dataConnect

            print ("intbl = " + intbl)

            # Process: Make Route Event Layer
            print ("Creating IRIS points")
            arcpy.MakeRouteEventLayer_lr(gbl.NdSTREETS+gbl.LRS_Routes, "IRIS_Road_Number", intbl, RdNumFld+" POINT "+BegMp, linref.point, OffSet, "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")

            linref.msg.elapsedTime = BeginTime.Stop()
            linref.msg.appendMessage = "Successfully created point event layer in " + linref.msg.elapsedTime + " seconds.\n"
            return linref
        except:
            linref.msg.appendMessage = "Did not create point route event layer.\n\n" + arcpy.GetMessages()
            linref.msg.fail = 1
            return linref

    elif lrType=="LINE":        #Processes route event layer for line data
        try:
            if dataConnect.find(".odc")!=-1:
                if tblName !="":
                    print ("Make table query if")
                    arcpy.MakeQueryTable_management(dataConnect+tblName, intbl, "ADD_VIRTUAL_KEY_FIELD", "", "", SQLqry)
                else:
                    print ("Make table query else")
                    arcpy.MakeQueryTable_management(dataConnect, intbl, "ADD_VIRTUAL_KEY_FIELD", "", "", SQLqry)

            else:
                if tblName !="":
                    print ("Make feature layer if ")
                    arcpy.MakeTableView_management(dataConnect+tblName, intbl, SQLqry)
                else:
                    print ("Make feature layer else")
                    arcpy.MakeTableView_management(dataConnect, intbl, SQLqry)

            # Process: Make Route Event Layer (2)
            print ("Creating IRIS lines")

            arcpy.MakeFeatureLayer_management(gbl.NdSTREETS+gbl.LRS_Routes, "lyr_"+gbl.LRS_Routes)
            print ("Feature layer made")
            arcpy.MakeRouteEventLayer_lr("lyr_"+gbl.LRS_Routes, "IRIS_Road_Number", intbl, RdNumFld+" LINE "+BegMp+" "+EndMp, linref.line, OffSet, "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")

##            arcpy.SaveToLayerFile_management (linref.line, "R:\\Temp\\"+linref.point+".lyr", "ABSOLUTE")

            linref.msg.elapsedTime = BeginTime.Stop()

            linref.msg.appendMessage = "Successfully created line event layer in " + linref.msg.elapsedTime + " seconds.\n"

            return linref

        except:
            linref.appendMessage = "Did not create line route event layer.\n\n" + arcpy.GetMessages()
            linref.fail = 1
            return linref

    elif lrType=="BOTH":        #Processes route event layer for both lines and points
        try:
            if SQLqry != "":
                SQLqry = " AND " + SQLqry

            if dataConnect.find(".odc")!=-1:

                if tblName !="":
                    arcpy.MakeQueryTable_management(dataConnect+tblName, intbl+"lines", "ADD_VIRTUAL_KEY_FIELD", "", "", BegMp+"<>"+EndMp+SQLqry)
                else:
                    intbllines = dataConnect
            else:
                if tblName !="":
                    arcpy.MakeTableView_management(dataConnect+tblName, intbl+"lines", BegMp+"<>"+EndMp+SQLqry)
##                arcpy.MakeQueryTable_management(dataConnect+tblName, intbl+"lines", "ADD_VIRTUAL_KEY_FIELD", "", "", )
                else:

                    arcpy.MakeTableView_management(dataConnect, intbl+"lines", BegMp+"<>"+EndMp+SQLqry)


            print ("Creating IRIS lines")
            arcpy.MakeRouteEventLayer_lr(gbl.NdSTREETS+gbl.LRS_Routes, "IRIS_Road_Number", intbl+"lines", RdNumFld+" LINE "+BegMp+" "+EndMp, linref.line, OffSet, "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")


            if dataConnect.find(".odc")!=-1:

                if tblName !="":
                    arcpy.MakeQueryTable_management(dataConnect+tblName, intbl+"pts", "ADD_VIRTUAL_KEY_FIELD", "", "", BegMp+"="+EndMp+SQLqry)
                else:
                    intblpts = dataConnect
            else:
                if tblName !="":
                    arcpy.MakeTableView_management(dataConnect+tblName, intbl+"pts", BegMp+"="+EndMp+SQLqry)
##                arcpy.MakeQueryTable_management(dataConnect+tblName, intbl+"lines", "ADD_VIRTUAL_KEY_FIELD", "", "", )
                else:

                    arcpy.MakeTableView_management(dataConnect, intbl+"pts", BegMp+"="+EndMp+SQLqry)

            print ("Creating IRIS points")

            arcpy.MakeRouteEventLayer_lr(gbl.NdSTREETS+gbl.LRS_Routes, "IRIS_Road_Number", intbl+"pts", RdNumFld+" POINT "+BegMp, linref.point, OffSet, "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")


            linref.msg.elapsedTime = BeginTime.Stop()

            linref.msg.appendMessage = "Successfully created route event layers in " + linref.msg.elapsedTime + " seconds.\n"

            return linref

        except:

            linref.appendMessage = "Did not create route event layers.\n\n" + arcpy.GetMessages + "\n"
            linref.fail = 1
            return linref

    else:

        linref.appendMessage = "Must use POINT, LINE or BOTH as first input parameter.\n"
