#-------------------------------------------------------------------------------
# Name:        StreetsAnno.py
# Purpose:     Update Streets Annotation from Nutsde.Production to Nutsde.Distribution
#
# Author:      RebekahM
#
# Created:     18/11/2011
# Copyright:   (c) RebekahB 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os, sys
cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import arcpy

from DataTransfer.modMoveData import GISDelete, GISCopy

import gbl, trktime
from modEmail import Send

try:
    # Local variables for Error Handling
    Title = "Streets Anno Log"
    Message = ""
    Error = 0
    EmailTo = gbl.MyEmail
    ScrptTimer = trktime.stopwatch()




    i=0
    while len(gbl.StreetsAnno)> i:

        print "Delete distribution feature class " + gbl.StreetsAnno[i]
        Temp = GISDelete(gbl.NdANNO_Streets+gbl.StreetsAnno[i])
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        print "Copy feature class from production to distribution"
        Temp = GISCopy(gbl.NpANNO_Streets+gbl.StreetsAnno[i],gbl.NdANNO_Streets+gbl.StreetsAnno[i])
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        i +=1

    #Adds a final script time to email
    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."

    print "All Done!!!"

    # Send email with successful operations
    Send(Title, Message, Error, EmailTo)


except:     # sends email with errors

    Error = Error + 1
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
    Send(Title, Message, Error, EmailTo)





