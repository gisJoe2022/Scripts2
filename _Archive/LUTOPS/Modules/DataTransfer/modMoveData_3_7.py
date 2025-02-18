# module MoveData.py
# provides functions to move data to and from different sde areas
#9/21/2011 ArcGIS 10.0.1

import os, sys
#cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
cmd_folder = "\\pwebgisapp1\GIS_Process_Scripts\PRODpyScriptShare\LUTOPS\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import arcpy
import gbl, trktime
from modEmail_3_7 import Send

arcpy.env.overwriteOutput=True


def GISDelete(     #Deletes a feature class
DeleteFC):          #Feature class to be deleted

    msg = gbl.PassMessage()
    t=trktime.stopwatch()

    try:

        if arcpy.Exists(DeleteFC):

            # Deletes feature class
            arcpy.Delete_management(DeleteFC, "FeatureClass")

            msg.elapsedTime = t.Stop()

            msg.appendMessage = DeleteFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully deleted in " + str(msg.elapsedTime) + " seconds.\n"
            return msg
        else:
            msg.appendMessage = DeleteFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " did not exist. No delete needed!\n"
            return msg

    except:

        msg.fail = 1
        msg.appendMessage = DeleteFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " did NOT delete.\n\n" + arcpy.GetMessages() + "\n"

        return msg



def GISDeleteFeatures(     #Deletes Features from a feature class
DeleteFC):                  #Feature class in which to delete features

    msg = gbl.PassMessage()
    t=trktime.stopwatch()

    try:
        if arcpy.Exists(DeleteFC):
            arcpy.ClearWorkspaceCache_management()
            # Process: Delete features

            arcpy.DeleteFeatures_management(DeleteFC)

        else:
            msg.fail = 1
            msg.appendMessage = "Data table does not exist"
            raise ValueError("Not able to connect to data source")

        msg.elapsedTime = t.Stop()
        msg.appendMessage = DeleteFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " features successfully deleted in " + str(msg.elapsedTime) + " seconds.\n"
        return msg

    except:

        msg.fail = 1
        msg.appendMessage = DeleteFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " features did NOT delete.\n\n" + arcpy.GetMessages() + "\n"
        return msg

def GISTruncate(     #Deletes Features from a feature class
DeleteFC):                  #Feature class in which to delete features

    msg = gbl.PassMessage()
    t=trktime.stopwatch()

    try:
        if arcpy.Exists(DeleteFC):
            arcpy.ClearWorkspaceCache_management()
            # Process: Delete features
            arcpy.TruncateTable_management(DeleteFC)
        else:
            msg.fail = 1
            msg.appendMessage = "Data table does not exist"
            raise ValueError("Not able to connect to data source")

        msg.elapsedTime = t.Stop()

        msg.appendMessage = DeleteFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " features successfully deleted in " + str(msg.elapsedTime) + " seconds.\n"
        return msg

    except:

        msg.fail = 1
        msg.appendMessage = DeleteFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " features did NOT delete.\n\n" + arcpy.GetMessages() + "\n"
        return msg

def GISAppendFeatures(     #Appends Features to an existing feature class

*args):

    msg = gbl.PassMessage()
    t = trktime.stopwatch()

    InFC=args[0]    #Input Feature class where features already exist
    OutFC=args[1]     #Output Feature class (target)
    FieldMap=""
##    FieldMap=args[2]
    print (len(args))
    if len(args)>2:
        FieldMap=args[2]
    else:
        FieldMap is None

    print ("FieldMap=" + FieldMap)


    if arcpy.Exists(InFC):
        if FieldMap is None:
            try:

                # Process: Append Features to feature class (no field mapping)
                arcpy.Append_management(InFC, OutFC, "NO_TEST", "", "")

                msg.elapsedTime = t.Stop()

                msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " features successfully appended in " + str(msg.elapsedTime) + " seconds.\n"
                return msg

            except:

                msg.fail = 1
                msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " features did NOT append.\n\n" + arcpy.GetMessages() + "\n"
                return msg
        else:

            try:

                # Process: Append Features to feature class (no field mapping)
                arcpy.Append_management(InFC, OutFC, "NO_TEST", FieldMap, "")

                msg.elapsedTime = t.Stop()

                msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " features successfully appended in " + str(msg.elapsedTime) + " seconds.\n"
                return msg

            except:

                msg.fail = 1
                msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " features did NOT append.\n\n" + arcpy.GetMessages() + "\n"
                return msg
    else:

        msg.fail = 1
        msg.appendMessage = "Data table does not exist"
        return msg
        raise ValueError("Not able to connect to data source")

def GISCopy(       #Copies feature class from one area to another
*args):

    InFC=args[0]               #Input feature class where features already exist
    OutFC=args[1]             #Output feature class
    GeomType=''                 #Configuration Keyword

    if len(args)>2:
        GeomType=args[2]
    else:
        GeomType=''

    msg = gbl.PassMessage()
    t= trktime.stopwatch()

    try:

        arcpy.CopyFeatures_management(InFC, OutFC,GeomType)

        msg.elapsedTime = t.Stop()

        msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully copied in " + str(msg.elapsedTime) + " seconds.\n"
        return msg

    except:

        msg.fail = 1
        msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not copied.\n\n" + arcpy.GetMessages() + "\n"

        return msg

def GISCopyAlt(       #Copies feature class from one area to another
*args):             #Output feature class

    InFC=args[0]
    OutFC=args[1]

    msg = gbl.PassMessage()
    t= trktime.stopwatch()

    print ("InFC is "+ InFC)
    print ("OutFC is "+ OutFC)

    try:
        if arcpy.Exists(InFC):
            arcpy.Copy_management(InFC, OutFC)

            msg.elapsedTime = t.Stop()

            msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully copied in " + str(msg.elapsedTime) + " seconds.\n"
            return msg
        else:
            msg.fail = 1
            msg.appendMessage = "Data table does not exist"
            raise ValueError("Not able to connect to data source")
    except:

        msg.fail = 1
        msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not copied.\n\n" + arcpy.GetMessages() + "\n"
        return msg

def GISCopyRows(       #Copies table from one area to another
InFC,               #Input feature class where features already exist
OutFC):             #Output feature class

    msg = gbl.PassMessage()
    t= trktime.stopwatch()

    try:
        if arcpy.Exists(InFC):
            arcpy.CopyRows_management(InFC, OutFC)


        else:
            msg.fail = 1
            msg.appendMessage = "Data table does not exist"
            raise ValueError("Not able to connect to data source")

        msg.elapsedTime = t.Stop()
        msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully copied in " + str(msg.elapsedTime) + " seconds.\n"
        return msg

    except:

        msg.fail = 1
        msg.appendMessage = OutFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not copied.\n\n" + arcpy.GetMessages() + "\n"

        return msg


def GISdeleteChangefc2fc( #makes feature class to feature class comparison and deletes changed and dropped features
DistFC, # distribution feature class; destination feature class
CreateFC, # comparison feature class; contains new data
dfcJoinFld, # distribution join field
cfcJoinFld, # comparison join field
SQLqry): # method of comparison using where clause; CHECKSUM

    dfc="dfc"
    cfc="cfc"
    msg = gbl.PassMessage()
    t = trktime.stopwatch()
    try:

        arcpy.MakeFeatureLayer_management(DistFC, dfc)

        arcpy.MakeFeatureLayer_management(CreateFC, cfc)


        arcpy.AddJoin_management(dfc, dfcJoinFld, cfc, cfcJoinFld,"KEEP_ALL")


        arcpy.SelectLayerByAttribute_management(dfc, "NEW_SELECTION", SQLqry)

        tmpCount =int(arcpy.GetCount_management(dfc).getOutput(0))
        print (tmpCount)
        if tmpCount >0:
            x=CreateFC.find(".sde\\")
            x=x+5
            print (CreateFC[x:])
            arcpy.RemoveJoin_management(dfc, CreateFC[x:])

            arcpy.DeleteFeatures_management(dfc)
        msg.elapsedTime = t.Stop()

        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully updated in " + str(msg.elapsedTime) + " seconds.\n"
        return msg
    except:

        msg.fail = 1
        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not updated.\n\n" + arcpy.GetMessages() + "\n"

        return msg


def GISaddChangefc2fc(#makes feature class to feature class comparison and updates changed and added features
DistFC, # distribution feature class; destination feature class
CreateFC, # comparison feature class; contains new data
dfcJoinFld, # distribution join field
cfcJoinFld, # comparison join field
SQLqry): # method of comparison using where clause; CHECKSUM)

    dfc="dfc"
    cfc="cfc"
    msg = gbl.PassMessage()
    t= trktime.stopwatch()


    try:
        arcpy.MakeFeatureLayer_management(DistFC, dfc)

        arcpy.MakeFeatureLayer_management(CreateFC, cfc)
        arcpy.AddJoin_management(cfc, cfcJoinFld, dfc, dfcJoinFld,"KEEP_ALL")

##        arcpy.CopyFeatures_management(cfc,CreateFC+"1")

        arcpy.SelectLayerByAttribute_management(cfc, "NEW_SELECTION", SQLqry)

        tmpCount =int(arcpy.GetCount_management(cfc).getOutput(0))
        print (tmpCount)

        if tmpCount > 0:
            x=DistFC.find(".sde\\") # provides needed format for removing join
            x=x+5
            print (DistFC[x:])
            arcpy.RemoveJoin_management(cfc, DistFC[x:])

            arcpy.Append_management(cfc, DistFC, "NO_TEST", "", "")
        msg.elapsedTime = t.Stop()

        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully updated in " + str(msg.elapsedTime) + " seconds.\n"
        return msg

    except:
        msg.fail = 1
        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not updated.\n\n" + arcpy.GetMessages() + "\n"

        return msg

def GISCalcfc2fc( #makes feature class to feature class comparison and deletes changed and dropped features
DistFC, # distribution feature class; destination feature class
CreateFC, # comparison feature class; contains new data
dfcJoinFld, # distribution join field
cfcJoinFld, # comparison join field
SQLqry,  # selection of calculation
calcfield, #field to be calculated
calcvalue): #value or expression to be calculated

    dfc="dfc"
    cfc="cfc"
    msg = gbl.PassMessage()
    t = trktime.stopwatch()
    try:

        arcpy.MakeFeatureLayer_management(DistFC, dfc)

        arcpy.MakeFeatureLayer_management(CreateFC, cfc)


        arcpy.AddJoin_management(dfc, dfcJoinFld, cfc, cfcJoinFld,"KEEP_ALL")


        arcpy.SelectLayerByAttribute_management(dfc, "NEW_SELECTION", SQLqry)

        tmpCount =int(arcpy.GetCount_management(dfc).getOutput(0))
        print (tmpCount)
        if tmpCount >0:
            x=CreateFC.find(".sde\\")
            x=x+5
            print (CreateFC[x:])
            arcpy.RemoveJoin_management(dfc, CreateFC[x:])


            arcpy.CalculateField_management(dfc,calcfield,calcvalue,"PYTHON_9.3")
        msg.elapsedTime = t.Stop()

        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully updated in " + str(msg.elapsedTime) + " seconds.\n"
        return msg
    except:

        msg.fail = 1
        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not updated.\n\n" + arcpy.GetMessages() + "\n"

        return msg

def CreateFieldMap(  #creates field map between two feature classes
JoinedLyr,
InFCSource,
InFCLayerName,
JoinTblName
):  #Input Feature Class

    msg = gbl.PassMessage
    t=trktime.stopwatch()
    InFC = InFCSource + InFCLayerName
    fieldMap = ""

    try:
        fl = arcpy.gp.listFields(JoinedLyr)

        for f in fl:
            fldNameLong = f.name
            fldType = f.type
            print (f.name)

            if fldNameLong.find(".")>0:
                fldNameShort= fldNameLong[fldNameLong.rfind(".")+1:]
            elif fldNameLong.find("dbo_")>-1:
                fldNameShort = fldNameLong[len(JoinTblName)+5:]
            else:
                fldNameShort = fldNameLong
            print (fldNameShort + "  " + fldType)
            if fldType =="String":
                fldType = "Text"
            if fldType =="Integer" and f.precision>5:
                fldType = "Long"

            if fldNameShort !="shape":
                fieldMap = fieldMap + fldNameShort + " " + fldNameShort +" " + str(f.editable).lower() + " "+ str(f.isNullable).lower() + " " + str(f.required).lower() + " " + str(f.length) + " " +fldType+ " " + str(f.scale) + " " + str(f.precision) + " ,First,#," + InFC.replace("\\","/") + "," + fldNameLong + ", -1, -1;"
                print (fieldMap)
        msg.rtnText = fieldMap

        msg.elapsedTime = t.Stop()

        msg.appendMessage = "Field map successfully updated in " + str(msg.elapsedTime) + " seconds.\n"


        print ("return Message")
        return msg

    except:
        msg.fail= 1
        msg.appendMessage = "Field map was not created! \n" + arcpy.GetMessages() + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

        print (msg.appendMessage)
        return msg


### Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
### The following inputs are layers or table views: "taxlots.taxlots_Layer"
#"TLNO /\TLNO/\ true true false 12 Text 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,distribution.taxlots.taxlots.TLNO,-1,-1;OBJECTID /\OBJECTID/\ false false false 4 Long 0 9 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,OBJECTID,-1,-1;PermitNumber /\PermitNumber/\ true true false 10 Text 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_PermitNumber,-1,-1;EnteredDate /\EnteredDate/\ true true false 16 Date 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_EnteredDate,-1,-1;AppliedDate /\AppliedDate/\ true true false 16 Date 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_AppliedDate,-1,-1;IssuedDate /\IssuedDate/\ true true false 16 Date 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_IssuedDate,-1,-1;Description /\Description/\ true true false 256 Text 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_Description,-1,-1;FeeAmount /\FeeAmount/\ true true false 8 Double 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_FeeAmount,-1,-1;TLID /\TLID/\ true true false 12 Text 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_TLID,-1,-1;Address /\Address/\ true true false 77 Text 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_Address,-1,-1;Location /\Location/\ true true false 128 Text 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_Location,-1,-1;Owner /\Owner/\ true true false 50 Text 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_Owner,-1,-1;PermitStatus /\PermitStatus/\ true true false 8 Text 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_PermitStatus,-1,-1;EnteredBy /\EnteredBy/\ true true false 12 Text 0 0 ,First,#,//Nutsde/GIS/Admin/ArcCatalog/ArcpySDEdbConnections/NdTaxlots.sde/distribution.taxlots.taxlots,dbo_v_ROW_No_Spray_EnteredBy,-1,-1","#")


def GISdeleteChangetbl2fc( #makes feature class to table comparison and deletes changed and dropped features
DistFC, # distribution feature class; destination feature class
tblFC, # comparison feature class; contains new data
dfcJoinFld, # distribution join field
cfcJoinFld, # comparison join field
SQLqry): # method of comparison using where clause; CHECKSUM

    dfc="dfc"
    cfc="cfc"
    msg = gbl.PassMessage()
    t = trktime.stopwatch()
    try:
        arcpy.ClearWorkspaceCache_management()
        print ("Make Feature Layer")
        arcpy.MakeFeatureLayer_management(DistFC, dfc)

        print ("Make Table View")
        arcpy.MakeQueryTable_management(tblFC, cfc,"ADD_VIRTUAL_KEY_FIELD","","","")

        print ("Add Join Management")
        arcpy.AddJoin_management(dfc, dfcJoinFld, cfc, cfcJoinFld,"KEEP_ALL")

        print ("Select by Layer")
        arcpy.SelectLayerByAttribute_management(dfc, "NEW_SELECTION", SQLqry)


        tmpCount =int(arcpy.GetCount_management(dfc).getOutput(0))
        print (tmpCount)
        if tmpCount >0:
##            x=tblFC.find(".odc\\")
##            x=x+5
##            print tblFC[x:]
            try:
                arcpy.RemoveJoin_management(dfc, cfc)
            except:
                pass
            print ("Delete features")
            arcpy.DeleteFeatures_management(dfc)
        msg.elapsedTime = t.Stop()
        print (msg.elapsedTime)

        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully updated in " + str(msg.elapsedTime) + " seconds.\n"
        return msg
    except:
        msg.fail = 1
        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not updated.\n\n" + arcpy.GetMessages() + "\n"

        return msg


def GISaddChangetbl2fc(#makes feature class to table comparison and updates changed and added features
DistFC, # distribution feature class; destination feature class
tblFC, # comparison feature class; contains new data
dfcJoinFld, # distribution join field
cfcJoinFld, # comparison join field
SQLqry): # method of comparison using where clause; CHECKSUM)

    dfc="dfc1"
    cfc="cfc1"
    msg = gbl.PassMessage()
    t= trktime.stopwatch()


    try:
        arcpy.ClearWorkspaceCache_management()
        arcpy.MakeFeatureLayer_management(DistFC, dfc)

        arcpy.MakeQueryTable_management(tblFC, cfc,"ADD_VIRTUAL_KEY_FIELD","","","")
        arcpy.AddJoin_management(cfc, cfcJoinFld, dfc, dfcJoinFld,"KEEP_ALL")

##        arcpy.CopyFeatures_management(cfc,CreateFC+"1")

        arcpy.SelectLayerByAttribute_management(cfc, "NEW_SELECTION", SQLqry)

        tmpCount =int(arcpy.GetCount_management(cfc).getOutput(0))
        print (tmpCount)

        if tmpCount > 0:
            x=DistFC.find(".sde\\") # provides needed format for removing join
            x=x+5
            print (DistFC[x:])
            arcpy.RemoveJoin_management(cfc, DistFC[x:])

        msg.rtnText = cfc
        msg.elapsedTime = t.Stop()

        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully updated in " + str(msg.elapsedTime) + " seconds.\n"
        return msg

    except:
        msg.fail = 1
        msg.appendMessage = DistFC.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not updated.\n\n" + arcpy.GetMessages() + "\n"

        return msg

def GISjoinFCtoTbl(*args #see variables below for definitions
    ):

    InFCSource=args[0]  # Feature class data path in which all records are kept
    InFCLayerName=args[1] #Feature class layer name
    InFld=args[2]       # Main table field on which to make join
    JoinTblSource=args[3]  # Table data path to be joined to main table
    JoinTblName=args[4] #Table name
    JoinFld=args[5]  # Join table field on which to make join

    if len(args)>6:
        KeepType=args[6] #Optional. Use for "KEEP_COMMON"
    else:
        KeepType="KEEP_ALL"
    try:
        t=trktime.stopwatch()
        Message=''
        msg = gbl.PassMessage()

        Temp=GISmfLyr(InFCSource,InFCLayerName,'')
        lyrInFC=Temp.rtnText
        Message = Message + Temp.appendMessage



        if JoinTblSource[-4:]!="dbo." :
            arcpy.MakeQueryTable_management(JoinTblSource+JoinTblName,'tblvw_'+JoinTblName, "ADD_VIRTUAL_KEY_FIELD")
            print ('Completed query table')
            tblvw ='tblvw_'+JoinTblName
        else:
            Temp1=GISmfLyr(JoinTblSource,JoinTblName,'')
            tblvw=Temp1.rtnText
            Message = Message + Temp.appendMessage

        arcpy.AddJoin_management(lyrInFC,InFld,tblvw,JoinFld,KeepType)
        print ('Completed join')

        msg.rtnText = lyrInFC
        msg.elapsedTime = t.Stop()
        Message = Message + ' successfully made join in ' + str(msg.elapsedTime) + ' seconds.\n'
        msg.appendMessage = Message

        return msg


    except:

        msg.fail = 1
        msg.appendMessage = "did not make join.\n\n" + arcpy.GetMessages() + "\n"

        return msg

##class GISJoin:
##
##    def __init__(self,MainTbl,  # Table in which all records are kept
##    JoinTbl,  # Table to be joined to main table
##    MainFld,  # Main table field on which to make join
##    JoinFld,  # Join table field on which to make join
##    MainQry,  # Where clause to restrict Main Table
##    JoinQry,    # Where clause to restrict Join table
##    JoinType): #Join Type KEEP_ALL or KEEP_COMMON
##        self.MainTbl = MainTbl
##        self.JoinTbl = JoinTbl
##        self.JoinFld = JoinFld
##        self.MainQry = MainQry
##        self.JoinQry = JoinQry
##        self.JoinType = JoinType
##
##    def GISJoinSqlTbltoTbl(self):
##        try:
##
##            self.msg = gbl.PassMessage()
##            t=trktime.stopwatch()
##            Mtbl = "Mtbl"
##            Jtbl = "Jtbl"
##
##            arcpy.ClearWorkspaceCache_management()
##            print "Main Table query"
##            arcpy.MakeQueryTable_management(MainTbl, "Mtbl","ADD_VIRTUAL_KEY_FIELD","","",MainQry)
##            print "Join Table query"
##            arcpy.MakeQueryTable_management(JoinTbl, "Jtbl","ADD_VIRTUAL_KEY_FIELD","","",JoinQry)
##            print "Join fields"
##            arcpy.AddJoin_management("Mtbl",MainFld, "Jtbl", JoinFld, JoinType)
##
##            print "print field list"
##            #Check field list
##            fl=arcpy.gp.listFields("Mtbl")
##            for f in fl:
##                fldNameLong = f.name
##                print fldNameLong
##
##            msg.rtnText = "Mtbl"
##            msg.elapsedTime = t.Stop()
##            msg.appendMessage = MainTbl.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully updated in " + msg.elapsedTime + " seconds.\n"
##            msg.appendMessage = msg.appendMessage + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
##            return msg
##        except:
##            msg.appendMessage = MainTbl.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not updated.\n\n" + arcpy.GetMessages() + "\n"
##            msg.appendMessage = msg.appendMessage + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
##            msg.fail = 1
##            return msg


def GISJoinSqlTbltoTbl(
    MainTbl,  # Table in which all records are kept
    JoinTbl,  # Table to be joined to main table
    MainFld,  # Main table field on which to make join
    JoinFld,  # Join table field on which to make join
    MainQry,  # Where clause to restrict Main Table
    JoinQry,  # Where clause to restrict Join table
    JoinType): # Join Type KEEP_ALL or KEEP_COMMON

        try:

            msg = gbl.PassMessage()
            t=trktime.stopwatch()

            Mtbl = "Mtbl"
            Jtbl = "Jtbl"
            print ("Main Table query")

            i=0
            while i!=1:
                if  arcpy.gp.exists(Mtbl):
                    Mtbl = Mtbl+"1"
                else:
                    i=1
            print (Mtbl)


            arcpy.MakeQueryTable_management(MainTbl, Mtbl,"ADD_VIRTUAL_KEY_FIELD","","",MainQry)
            print ("Join Table query")
            arcpy.MakeQueryTable_management(JoinTbl, "Jtbl","ADD_VIRTUAL_KEY_FIELD","","",JoinQry)
            print ("Join fields")
            arcpy.AddJoin_management(Mtbl,MainFld, "Jtbl", JoinFld, JoinType)

            print ("print field list")
            #Check field list
            fl=arcpy.gp.listFields("Mtbl")
            for f in fl:
                fldNameLong = f.name
                print (fldNameLong)

            msg.rtnText = Mtbl
            msg.elapsedTime = t.Stop()
            msg.appendMessage = MainTbl.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " successfully updated in " + str(msg.elapsedTime) + " seconds.\n"
            msg.appendMessage = msg.appendMessage + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
            return msg
        except:
            msg.fail = 1
            msg.appendMessage = MainTbl.replace("\\\\emcgis\\nas\\LUTOPS\\GIS\\Admin\\ArcCatalog\\ArcpySDEdbConnections\\","") + " was not updated.\n\n" + arcpy.GetMessages() + "\n"
            msg.appendMessage = msg.appendMessage + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

            return msg

def GISmfLyr(           #Make feature layer required for funcitonality of SQL geometry layers
    InFCSource,      #Input file path
    InFCLayerName,   #Layer name or feature class
    SQLqry
 ):
    print (InFCSource)
    print (InFCLayerName)

    msg = gbl.PassMessage()
    t=trktime.stopwatch()
    out_lyr =''

    try:
        out_lyr='lyr_'+InFCLayerName.rstrip('.lyr')
        print (out_lyr)
        arcpy.MakeFeatureLayer_management(InFCSource+InFCLayerName,out_lyr,SQLqry)

        msg.rtnText = out_lyr
        msg.appendMessage = out_lyr + ' successfully made a feature layer in ' + str(msg.elapsedTime) + ' seconds.\n'

        return msg

    except:
        msg.fail = 1
        msg.appendMessage = out_lyr + " did not make a feature layer.\n\n" + arcpy.GetMessages() + "\n"

        return msg


def  GISspFldJoinPtPoly(               #takes attribute information from a polygon layer and calculates to a point layer
        InFCSource,                    #input point feature class file path
        InFCLayerName,                 #input feature class name
        InFld,                         #field to be calculated
        PolyFCSource,                  #polygon feature class file path
        PolyFCLayerName,               #polygon feature class name
        PolyFld                        #polygon field data to transfter in calculated field; field type must be same as InFld
        ):

    t=trktime.stopwatch()
    Message=''

    try:

        Temp =GISmfLyr(PolyFCSource,PolyFCLayerName,'')
        lyrPolyFC = Temp.rtnText
        Message = Message + Temp.appendMessage

        print ('Make feature layer polygon completed')
        Temp1=GISmfLyr(InFCSource,InFCLayerName,'')
        lyrInFC=Temp1.rtnText
        Message = Message + Temp1.appendMessage

        print ('Make feature layer point completed')
        msg = gbl.PassMessage()
        print ('past msg variable')

        print (PolyFCSource+PolyFCLayerName)
        rows =arcpy.SearchCursor(PolyFCSource+PolyFCLayerName)
        #'print past search cursor')
        for row in rows:
            #selections are cleared from layers
            arcpy.SelectLayerByAttribute_management(lyrPolyFC,'CLEAR_SELECTION')
            arcpy.SelectLayerByAttribute_management(lyrInFC,'CLEAR_SELECTION')
            print ('Selections cleared')
            #get value from row
            CalcVal=row.getValue(PolyFld)
            print (CalcVal)
            #Select polygon in getvalue
            print (PolyFld + '= \''+ CalcVal+ '\'')
            if isinstance(CalcVal,basestring):
                arcpy.SelectLayerByAttribute_management(lyrPolyFC,'NEW_SELECTION', PolyFld + '= \''+ CalcVal+ '\'')
            else:
                arcpy.SelectLayerByAttribute_management(lyrPolyFC,'NEW_SELECTION', PolyFld + '='+ CalcVal)
            #Select points by polygon selection
            print ('Select by location')
            arcpy.SelectLayerByLocation_management(lyrInFC,'INTERSECT',lyrPolyFC,0,'NEW_SELECTION')
            #Calculate values
            print ('Calc value')
            if isinstance(CalcVal,basestring):
                arcpy.CalculateField_management(lyrInFC,InFld,'\'' + CalcVal + '\'','PYTHON_9.3')
            else:
                arcpy.CalculateField_management(lyrInFC,InFld,CalcVal,'PYTHON_9.3')

        if row:
            del row
        if rows:
            del rows
        msg.elapsedTime = t.Stop()
        msg.appendMessage = Message + '\n '+ InFld + 'values calculated'+ ' successfully made a feature layer in ' + str(msg.elapsedTime) + ' seconds.\n'

        return msg

    except:
        msg.fail = 1
        msg.appendMessage = InFld + " values did not calculate.\n\n" + arcpy.GetMessages() + "\n"

        return msg

