#-------------------------------------------------------------------------------
# Name:        taxlotSQLgeom
# Purpose:      Create Web Mercator SQL Geometry taxlots for use in SQL joins
#
# Author:      RebekahM
#
# Created:     14/02/2014
# Copyright:   (c) RebekahM 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os, sys
cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Import arcpy module
import arcpy, trktime, gbl
from modEmail import Send
from DataTransfer.modMoveData import GISDelete, GISTruncate, GISAppendFeatures

Title = "TaxlotsSQLgeom Log"
Message = ""
Error = 0
ScrptTimer = trktime.stopwatch()
EmailTo = gbl.MyEmail

#GIS variables
InFC = gbl.WdTAXLOTS+gbl.taxlots
OutFC = gbl.NpTAXLOTS+gbl.taxlots_msGeom_WMAS
InVW=gbl.NpTAXLOTS+"TAX_SHAPEF_VIEW_4web"
OutVW=gbl.NpTAXLOTS+"TAX_SHAPEF_VIEW_WMAS"

try:

    if arcpy.gp.exists(InFC):

        if arcpy.gp.exists(OutFC):

             # Deletes features from production.taxlots.taxlots_msGeom_WMAS
            print "Delete production taxlots"
            Temp = GISDelete(OutFC)
            Message = Message + Temp.appendMessage
            Error = Error + Temp.fail
        else: #when OutFC does not exist
            Message = Message+ "\n No feature class found in production"


        print "Project Taxlots"
        GetCS = arcpy.Describe(InFC)
        InCS = GetCS.spatialReference
        OutCS = arcpy.SpatialReference(3857)
        print OutCS.name
        print InCS.name
        print
        print InFC
        print OutFC
        print "Project to WMAS"
        arcpy.Project_management(InFC,OutFC,OutCS,"NAD_1983_HARN_To_WGS_1984",InCS)

        arcpy.ClearWorkspaceCache_management()

##        print "Start integrate"
##        arcpy.Integrate_management(in_features=OutFC +" #", cluster_tolerance="0.5 Meters")
##        print "End integrate"


        arcpy.AddIndex_management(OutFC, "TLNO", "ndx_TLNO", "NON_UNIQUE","NON_ASCENDING")

        if arcpy.gp.exists(InVW):
            if arcpy.gp.exists(OutVW):
                if int(arcpy.GetCount_management(InVW).getOutput(0))>100000:
                        print "Delete features from GisBug"
                        Temp = GISTruncate(OutVW)
                        Message = Message + Temp.appendMessage
                        Error = Error + Temp.fail

                        if Error==0:
                            print "Append features to distribution"
                            Temp = GISAppendFeatures(InVW,OutVW)
                            Message = Message + Temp.appendMessage
                            Error = Error + Temp.fail

                            try:
##                                        sqlconn=arcpy.ArcSDESQLExecute(gbl.dcNpTAXLOTS)
##                                        print "Created sql connection"
##
##                                        sql="""Grant SELECT on taxlots.TAXLOTS_MSGEOM_WMAS TO OPS"""
##
##                                        sqlconn.execute(sql)
##
##                                        print "Permissions applied"

                                arcpy.ChangePrivileges_management(OutFC,"OPS","GRANT","AS_IS")

                            except:
                                Message = Message + "Grant Select on OPS did not execute"

                        else:
                            raise ValueError("There was a failure when truncating. Table did not update")
                else:
                    raise ValueError("Incomplete data in view")
            else:
                raise ValueError("Was not able to access Nutsde.production.taxlots.Tax_Shapef_vw")


        else: #When InFC is not available
            Message = Message + "\n !!! Taxlots do not exist. Cannot Update"
            Error = Error+1


#Adds a final script time to email
    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."

    print "All Done!!!"

# Send email with successful operations
    Send(Title, Message, Error, EmailTo)

except:  #send email with errors

    EmailTo #+ ",Wayne_Flynn@co.washington.or.us"
    Error = Error + 1
    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

    Send(Title, Message, Error, EmailTo)
