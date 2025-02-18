#-------------------------------------------------------------------------------
# Name:        intersections.py
# Purpose:     Creates intersection feature classes from Streets.WashStr
#
# Author:      RebekahM
#
# Created:     20/03/2012
# Copyright:   (c) RebekahM 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os, sys
cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from time import clock

# Import arcpy module
import arcpy
from arcpy import env

# Import custom modules
import gbl, trktime
from DataTransfer.modMoveData import GISDelete, GISCopy, GISDeleteFeatures, GISAppendFeatures,GISCalcfc2fc,GISTruncate,GISmfLyr
from modEmail import Send

try:
    StrNames = "StrNames"

    Title = "Intersections Script Log"
    Message = ""
    Error = 0
    ScrptTimer = trktime.stopwatch()
    EmailTo = gbl.MyEmail
##    EmailTo="rebekah_bishop@co.washington.or.us"

    arcpy.gp.overwriteOutput = True

    # Variable Reference
    # strNames = WashStr
    # Xsect = intersections
    # strInt = StrNamesdissolve

    FCchk = int(arcpy.GetCount_management(gbl.NdSTREETS+gbl.WashStr).getOutput(0))#Checks for data in data source
    if FCchk >0:

        pstart = clock()
         # Deletes features from production.Streets_QC.intersections
        print "Delete Unique name points"
        Temp = GISDelete(gbl.NpSTREETSQC+StrNames+"pts")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail
        ptime = str(round(clock()-pstart,2))
        print "Process time: " + ptime

        pstart = clock()


        # Make feature layer of named streets
        print "Make Feature layer of Named Streets"
        arcpy.MakeFeatureLayer_management(gbl.NdSTREETS+gbl.WashStr, StrNames, "FName <> '' AND Type NOT IN (1321,1421,1471,1521)")
        ptime = str(round(clock()-pstart,2))
        print "Process time: " + ptime

        pstart = clock()
        #Dissolve like named streets
        print "Dissolve like named streets"
        arcpy.Dissolve_management(StrNames, gbl.NpSTREETSQC+StrNames,["FDPRE","FNAME","FTYPE","FDSUF"],"","SINGLE_PART", "DISSOLVE_LINES")

        #Split Lines
        print "Split lines at named intersections"
        arcpy.FeatureToLine_management(gbl.NpSTREETSQC+StrNames,gbl.NpSTREETSQC+StrNames+"Split","","ATTRIBUTES")

        # Convert to Points
        print "Convert lines to points"
        arcpy.FeatureVerticesToPoints_management(gbl.NpSTREETSQC+StrNames+"Split",gbl.NpSTREETSQC+StrNames+"pts","BOTH_ENDS")
        ptime = str(round(clock()-pstart,2))
        print "Process time: " + ptime

        pstart = clock()
        # Convert to Points
        print "Convert lines to points"
        arcpy.FeatureVerticesToPoints_management(StrNames,gbl.NpSTREETSQC+StrNames+"pts","BOTH_ENDS")
        ptime = str(round(clock()-pstart,2))
        print "Process time: " + ptime


        pstart = clock()
        arcpy.AddIndex_management(gbl.NpSTREETSQC+StrNames+"pts", "LOCALID","index_localID", "NON_UNIQUE", "ASCENDING")
        # Calculate Values

        sqlconn=arcpy.ArcSDESQLExecute(gbl.dcNpSTREETSQC)
        print "Created sql connection"

        sqlconn.startTransaction()
        print "SQL Transaction started"

        sql="""EXEC streets_qc.proc_XsectID_update """

        try:
            print "Try to execute SQL Transaction"
            sqlreturn=sqlconn.execute(sql)

        except Exception as err:
            print err
            Message=Message + err
            sqlreturn=False
            Error=Error+1

        if sqlreturn==True:
            print "SQL statement successfully executed"
            sqlconn.commitTransaction()
            Message= Message + "\n SQL update ran successfully"
        else:
            Message = Message + "SQL execute failed"
            raise NameError("\n SQL did not execure successfully")

#Update feature classes

        print "Delete features production Intersections Unique"
        Temp = GISTruncate(gbl.NpSTREETS+gbl.IntersectionUnique)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail


        print "Append features to production Intersections Unique"
        Temp = GISAppendFeatures(gbl.NpSTREETSQC+"Int_"+gbl.IntersectionUnique+"_vw", gbl.NpSTREETS+gbl.IntersectionUnique)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail


        print "Delete features production XsectID"
        Temp = GISTruncate(gbl.NpSTREETS+gbl.XsectID)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail


        print "Append features to production Intersections Unique"
        Temp = GISAppendFeatures(gbl.NpSTREETSQC+gbl.XsectID, gbl.NpSTREETS+gbl.XsectID)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        print "Make intersection fearture layer"
        Temp = GISmfLyr(gbl.NpSTREETSQC, gbl.XsectID, "Active=1")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        print "Delete features production intersections"
        Temp = GISTruncate(gbl.NpSTREETS+gbl.intersections)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        print "Append features to production Intersections"
        Temp = GISAppendFeatures("lyr_XsectID", gbl.NpSTREETS+gbl.intersections)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        print "Stage for psqlgis1"
        Temp=GISDelete(gbl.NpSTREETS+"intersections_id")
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        arcpy.Project_management(in_dataset=gbl.NpSTREETS+gbl.XsectID, out_dataset=gbl.NpSTREETS+"intersections_id", out_coor_system="PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',8202099.737532808],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Foot',0.3048]]", transform_method="", in_coor_system="PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',8202099.737532808],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Foot',0.3048]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")

#*****Distribution updates*******
        print "Delete features production Intersections Unique"
        Temp = GISTruncate(gbl.NdSTREETS+gbl.IntersectionUnique)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail


        print "Append features to production Intersections Unique"
        Temp = GISAppendFeatures( gbl.NpSTREETS+gbl.IntersectionUnique, gbl.NdSTREETS+gbl.IntersectionUnique)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail


        print "Delete features production XsectID"
        Temp = GISTruncate(gbl.NdSTREETS+gbl.XsectID)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail


        print "Append features to production Intersections Unique"
        Temp = GISAppendFeatures(gbl.NpSTREETS+gbl.XsectID,gbl.NdSTREETS+gbl.XsectID)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        print "Delete features production intersections"
        Temp = GISTruncate(gbl.NdSTREETS+gbl.intersections)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail

        print "Append features to production Intersections"
        Temp = GISAppendFeatures(gbl.NpSTREETS+gbl.intersections,gbl.NdSTREETS+gbl.intersections)
        Message = Message + Temp.appendMessage
        Error = Error + Temp.fail




    else:
        Message = "No data in source feature class!/n" + Message
        Error = Error + 1



    #Adds a final script time to email
    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."

    print "All Done!!!"

    # Send email with successful operations
    Send(Title, Message, Error, EmailTo)





except:

    print Message

    Send(Title, Message, Error, EmailTo)



