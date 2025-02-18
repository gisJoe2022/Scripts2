#-------------------------------------------------------------------------------
# Name:        GISbugTransporUpdate.py
# Purpose:     Updates GISbug for other jurisdiction use.
#
# Author:      RebekahB
#
# Created:     07/04/2020
# Copyright:   (c) RebekahB 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

try:
    import os, sys
    cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)

    # Import system modules
    import arcpy, smtplib, string,gbl,trktime
    from DataTransfer.modMoveData import GISAppendFeatures, GISTruncate, GISmfLyr
    from modEmail import Send

    arcpy.env.overwriteOutput=True

    Title = "GISbug update"
    Message = ""
    Error = 0
    EmailTo = gbl.MyEmailRyan
    ScrptTimer = trktime.stopwatch()


  ## .lyr file name and GISbug feature class name must be the same.

    for r,d,f in os.walk('\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\Transpor\\GISBUG'):
        InFCSouce= r+'\\'
        for item in f:
            if '.lyr' in item:
                InFCLayerName=item
                lyrName= item.replace('.lyr','')

                print ("Make feature layer gisbug.transpor." +lyrName)
                GIStemp = GISmfLyr(InFCSouce,InFCLayerName,"")
                lyrGIS = GIStemp.rtnText
                Message = Message + GIStemp.appendMessage
                Error = Error + GIStemp.fail

                if Error>0:
                    raise NameError('GIS make feature layer failed')

                if arcpy.gp.exists(gbl.WBUG_TRANSPOR+lyrName):
                    if int(arcpy.GetCount_management(lyrGIS).getOutput(0))>0 or int(arcpy.GetCount_management(gbl.WBUG_TRANSPOR+lyrName).getOutput(0))<10:

                        print ("Delete features from GISbug " + lyrName)
                        Temp = GISTruncate(gbl.WBUG_TRANSPOR+lyrName)
                        Message = Message + Temp.appendMessage
                        Error = Error + Temp.fail

                       # Appends features to GISBUG.TRANSPOR.WC_Pavement
                        print ("Append features to GISbug " + lyrName)
                        Temp = GISAppendFeatures(lyrGIS, gbl.WBUG_TRANSPOR+lyrName)
                        Message = Message + Temp.appendMessage
                        Error = Error + Temp.fail
                    else:
                        raise NameError('No records in dataset and previous recordset had more than 10 records. Please verify update with source info and adjust code if necessary')
                else:
                    raise NameError('Not able to access output database')

#Adds a final script time to email
    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."

    print ("All Done!!!")

# Send email with successful operations
    Send(Title, Message, Error, EmailTo)

except:  #send email with errors

    EmailTo = EmailTo #+ ",Brian_Hanes@co.washington.or.us,Richard_Crucchiola@co.washington.or.us,Russell_Campbell@co.washington.or.us"
    Error = Error + 1
    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

    Send(Title, Message, Error, EmailTo)


