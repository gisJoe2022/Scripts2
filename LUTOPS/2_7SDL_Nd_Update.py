# ---------------------------------------------------------------------------
# SDL_Nd_Update.py - Updates SDL lights from production
# Created on: Wed Jun 16 2010 09:14:24 AM
#   last updated for ArcGIS 10.2.0 - Win7 64 bit
# ---------------------------------------------------------------------------

#Allows importing of custom modules
import os, sys
cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy
from arcpy import env

# Import custom modules
import gbl, trktime
from DataTransfer.modMoveData import GISDelete, GISCopy, GISDeleteFeatures, GISAppendFeatures
from DataTransfer.mod_lin_ref_IRIS import IRIS_lin_ref
from modEmail import Send


Title = "SDL Lighting"
Message = ""
Error = 0
EmailTo = gbl.MyEmail
ScrptTimer = trktime.stopwatch()


try:
##
##    # Deletes features from distribution.TRANSPOR.PMSAll_Roads
##    print "Delete features from distribution"
##    Temp = GISDeleteFeatures(gbl.NdSDL+gbl.SDL_lights)
##    Message = Message + Temp.appendMessage
##    Error = Error + Temp.fail
##
##    # Appends features to distribution.TRANSPOR.PMSAll_Roads
##    print "Append features to distribution"
##    Temp = GISAppendFeatures(gbl.NpSDL+gbl.SDL_lights, gbl.NdSDL+gbl.SDL_lights)
##    Message = Message + Temp.appendMessage
##    Error = Error + Temp.fail

    # Deletes features from distribution.TRANSPOR.PMSAll_Roads
    print "Delete features from distribution"
    Temp = GISDeleteFeatures(gbl.NdSDL+gbl.SDL_AsmntArea)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Appends features to distribution.TRANSPOR.PMSAll_Roads
    print "Append features to distribution"
    Temp = GISAppendFeatures(gbl.NpSDL+gbl.SDL_AsmntArea, gbl.NdSDL+gbl.SDL_AsmntArea)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    #Adds a final script time to email
    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."

    print "All Done!!!"

except:

##    EmailTo + ",Wayne_Flynn@co.washington.or.us,Richard_Crucchiola@co.washington.or.us"
    Error = Error + 1
    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

    Send(Title, Message, Error, EmailTo)



