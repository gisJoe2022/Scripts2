#-------------------------------------------------------------------------------
# Name:        CPM.py
# Purpose:     Updates CPM line and points from GAP/TIM where CPM maintains their project data.
#
# Author:      RebekahM
#
# Created:     03/05/2012
# Copyright:   (c) RebekahM 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

try:

    import os, sys
    cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)

    # Import arcpy module
    import arcpy
    from arcpy import env

    # Import custom modules
    import gbl, trktime
    from DataTransfer.modMoveData import GISDelete, GISCopy, GISDeleteFeatures, GISAppendFeatures, GISTruncate
    from modEmail import Send



    Title = "Capital Projects Log"
    Message = ""
    Error = 0
    ScrptTimer = trktime.stopwatch()
    EmailTo = gbl.MyEmail

    lines = "_lines"
    pts = "_pts"
    area = "_areas"


    # Deletes production.Transpor.CPM
    print("Truncates data")
    Temp = GISTruncate(gbl.NpTRANSPOR+gbl.TIM_lines)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    print ("Append features to distribution")
    Temp = GISAppendFeatures(gbl.Wp+gbl.TRANSPOR_TIM_Lines, gbl.NpTRANSPOR+gbl.TIM_lines)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    # Deletes production.Transpor.CPM
    print("Truncates data")
    Temp = GISTruncate(gbl.NpTRANSPOR+gbl.TIM_points)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    arcpy.Dissolve_management(gbl.Wp+gbl.TRANSPOR_TIM_points, gbl.NpTRANSPOR+gbl.TIM_points,dissolve_field="Status_0;Source_1;Issue_1;nType_1;LID_1;forPub_1;Count_1;stName_1;fromST_1;toST_1;IRISno_1;Fclass_1;xLanes_1;pLanes_1;URMD_1;CntyRd_1;TDT_1;multiJur_1;ageInv_1;jurMain_1;comDist_1;projOverL_1;nNotes_1;nCat_2;PIMP_2;PIMPdate_2;intSol_2;ROW1_2;ROW2_2;genCostEst_2;genCostEstDate_2;psNotes_2;AFsource1_3;AFsource2_3;AFsource3_3;projPeriod_3;cNotes_3;projName_4;projNo_4;projBudg_4;projBudgDate_4;projBidDate_4;costEst_4;costEstDate_4;projStartDate_4;projConStartDate_4;projContacts_4;projHypr_4;comNotes_4;compDate_5;finalCost_5;compNotes_5;CIP_6;TIM3_List1;TIM3_List1yr;TIM3_List2;TIM3_List2yr;TIM3_List3;TIM3_List3yr;TIM3_List4;TIM3_List4yr;TIM3_List5;TIM3_List5yr;TIM3_List6;TIM3_List6yr;Data_Steward_1;MLID_1", statistics_fields="", multi_part="MULTI_PART")


##    print "Append features to distribution"
##    Temp = GISAppendFeatures('In_Memory\\TimPointsDissolve', gbl.NpTRANSPOR+gbl.TIM_points)
##    Message = Message + Temp.appendMessage
##    Error = Error + Temp.fail

    # Deletes production.Transpor.CPM
    print("Delete production.Transpor.CPM")
    Temp = GISTruncate(gbl.NpTRANSPOR+gbl.CPM_Projects+lines)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    print("Append features to distribution")
    Temp = GISAppendFeatures(gbl.NpTRANSPOR+gbl.CPM_projects_lines_vw,gbl.NpTRANSPOR+gbl.CPM_Projects+lines)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

##    Depricated
##    arcpy.MakeFeatureLayer_management (gbl.fgdbCPM+gbl.CPM_Projects,"CPMprj")
##
##    arcpy.SelectLayerByAttribute_management("CPMprj","NEW_SELECTION", "For_Public_Consumption = 1")

##    print "Copy CPM projects to production"
##    Temp = GISCopy("CPMprj", gbl.NpTRANSPOR+gbl.CPM_Projects+lines)
##    Message = Message + Temp.appendMessage
##    Error = Error + Temp.fail

   # Deletes features from production
    print("Delete features from distributon")
    Temp = GISTruncate(gbl.NdTRANSPOR+gbl.CPM_Projects+lines)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    print("Append features to distribution")
    Temp = GISAppendFeatures(gbl.NpTRANSPOR+gbl.CPM_Projects+lines, gbl.NdTRANSPOR+gbl.CPM_Projects+lines)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

##
##
###______________________________________________________________________________
###   Create CPM points

    # Deletes production.Transpor.CPM
    print("Delete production.Transpor.CPM)
    Temp = GISDelete(gbl.NpTRANSPOR+gbl.CPM_Projects+pts)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    print("Create CPM points")

    arcpy.FeatureToPoint_management(gbl.NdTRANSPOR+gbl.CPM_Projects+lines, gbl.NpTRANSPOR+gbl.CPM_Projects+pts, "INSIDE")

   # Deletes features from production
    print("Delete features from distributon")
    Temp = GISTruncate(gbl.NdTRANSPOR+gbl.CPM_Projects+pts)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    print("Append features to distribution")
    Temp = GISAppendFeatures(gbl.NpTRANSPOR+gbl.CPM_Projects+pts, gbl.NdTRANSPOR+gbl.CPM_Projects+pts)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    #Adds a final script time to email
    TtlScrptTime = ScrptTimer.Stop()
    Message = Message + "Total processing time : " + TtlScrptTime + " seconds."

    print(Message)
    print("All Done!!!")

    # Send email with successful operations
    Send(Title, Message, Error, EmailTo)

except:
    EmailTo = EmailTo # + ",Brian_Hanes@co.washington.or.us,Richard_Crucchiola@co.washington.or.us,Russell_Campbell@co.washington.or.us,steven_cotterill@washingtoncountyor.gov"
    Error = Error + 1
    Message = Message + arcpy.GetMessages()
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

    Send(Title, Message, Error, EmailTo)





