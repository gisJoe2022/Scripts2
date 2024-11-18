#-------------------------------------------------------------------------------
# Name:        mod_local.py
# Purpose:     functions for local processing
#
# Author:      RebekahM
#
# Created:     06/01/2014
# Copyright:   (c) RebekahM 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os, sys
#cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import tempfile, arcpy, gbl

class gisTemp:
    msg = gbl.PassMessage()
    tempLoc = ""
tmpGIS = gisTemp()


def tmpGISwkspace(): #creates GIS folder and local workspace in Temp area

    tmpGIS.tempLoc=str(tempfile.gettempdir())

    try:
#creates GIS folder
        if arcpy.Exists(tmpGIS.tempLoc+"\\ArcGIS\\"):
            tmpGIS.tempLoc=tmpGIS.tempLoc+"\\ArcGIS\\"
            print ("GIS folder exists")
        else:
            arcpy.CreateFolder_management(tmpGIS.tempLoc,"ArcGIS")
            tmpGIS.tempLoc=tmpGIS.tempLoc+"\\ArcGIS\\"
            
            tmpGIS.msg.appendMessage = "Created GIS folder.\n"
            print ("GIS folder created")

#creates local file geodatabase
        try:
            if arcpy.Exists(tmpGIS.tempLoc+"Default.gdb"):
                print ('Delete default.gdb')
                arcpy.Delete_management(tmpGIS.tempLoc+"Default.gdb",)
                print ('Create default.gdb')
                arcpy.CreateFileGDB_management(tmpGIS.tempLoc, "Default.gdb","CURRENT")
                tmpGIS.tempLoc=tmpGIS.tempLoc+"Default.gdb\\"
                tmpGIS.msg.appendMessage = tmpGIS.msg.appendMessage+"Temp default fgdb replaced.\n"
                print ("Default File geodatabase exists")
            else:
                arcpy.CreateFileGDB_management(tmpGIS.tempLoc, "Default.gdb","CURRENT")
                tmpGIS.tempLoc=tmpGIS.tempLoc+"Default.gdb\\"
                tmpGIS.msg.appendMessage = tmpGIS.msg.appendMessage+"Created default file geodatabase.\n"
                print ("Default File geodatabase created")
            return tmpGIS
        except:
            tmpGIS.msg.appendMessage = tmpGIS.msg.appendMessage+"Did not default file geodatabase.\n"
            tmpGIS.msg.fail = 1
            print ("fgdb failure")
            return tmpGIS

    except:
        tmpGIS.msg.appendMessage = tmpGIS.msg.appendMessage+"Did not create ArcGIS folder.\n"
        tmpGIS.msg.fail = 1
        print ("ArcGIS folder failure")
        return tmpGIS





