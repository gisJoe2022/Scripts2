# coding=utf-8
# -------------------------------------------------------------------------------
"""
Name:           Updates UPAA Cities

Purpose:        Updates Cities in Production.Boundary.UPAA then pushes to 
                Distribution.Boundary.UPAA

Description:    

Author:         Josephh, Washington County 2021

Created:        2021-04-20
Updated:		2021-07-01 JH
"""
# -------------------------------------------------------------------------------

# Import modules
import arcpy
from sys import argv

# Define Input Parameters

# Variables
UPAA_Prod = r'Database Connections\\tsqlgis1_production_boundary.sde\\Production.BOUNDARY.UPAA_1_Prod'
UPAA_Dist= r'Database Connections\\tsqlgis1_production_boundary.sde\\Production.BOUNDARY.UPAA_1_Dist'
DistCity = r'Database Connections\\tsqlgis1_production_boundary.sde\\Production.BOUNDARY.cities'

UPAA_Prod_layer = "UPAA_Prod_layer"
UPAA_Dist_layer = "UPAA_Dist_layer"
DistCity_layer = "DistCity_layer"


UPAA_Prod="UPAA_Update_test_Prod"
UPAA_Dist="J:\\Workgroups\\GISPlanning\\GIS\\GIS_Data_Updates_Pro\\LUD_Edits.gdb\\UPAA_Update_test_Dist"
Cities="distribution.BOUNDARY.cities"


# SDE UPAA w/City 
def SDEUPAAwCity():  

    # OverwriteOutput
    arcpy.env.overwriteOutput = True


    # Make Production UPAA Feature Layer
    arcpy.management.MakeFeatureLayer(UPAA_Prod, UPAA_Prod_layer)

    # Make Distribution UPAA Feature Layer
    arcpy.management.MakeFeatureLayer(UPAA_Prod, UPAA_Prod_layer)

    # Make City Feature Layer
    arcpy.management.MakeFeatureLayer(DistCity, DistCity_layer)

    # Select All Cities, except Portland, By Attributte
    arcpy.management.SelectLayerByAttribute(UPAA_Prod_layer, "NEW_SELECTION", "LABEL = 'City' And CITY <> 'PORTLAND'")

    # Delete Selected City Rows
    arcpy.management.DeleteRows(UPAA_Prod_layer)[0]

    # Select All NEW Cities, except Portland, Layer By Attribute
    arcpy.management.SelectLayerByAttribute(DistCity, "NEW_SELECTION", "JURNAME <> 'Portland'")

    # Append NEW City Boundaries to Production UPAA
    arcpy.management.Append(inputs=[distribution_BOUNDARY_cities_2_], target=Updated_Input_With_Rows_Removed_2_, schema_type="NO_TEST", field_mapping="CITY \"CITY\" true true false 20 Text 0 0,First,#,distribution.BOUNDARY.cities,JURNAME,0,255;created_user \"created_user\" true true false 255 Text 0 0,First,#;created_date \"created_date\" true true false 8 Date 0 0,First,#;last_edited_user \"last_edited_user\" true true false 255 Text 0 0,First,#;last_edited_date \"last_edited_date\" true true false 8 Date 0 0,First,#;ACRES \"ACRES\" true true false 8 Double 0 0,First,#,C:\\Users\\josephh\\AppData\\Local\\Temp\\ArcGISProTemp14392\\e512dbec3ffe96b0487dfceef062ced5.sde\\distribution.BOUNDARY.cities,ACRES,-1,-1;LABEL \"LABEL\" true true false 10 Text 0 0,First,#;YEAR \"YEAR\" true true false 2 Short 0 0,First,#;LINK \"LINK\" true true false 500 Text 0 0,First,#", subtype="", expression="")[0]


    #____________________MB Output Starts Here__________________

    UPAA_Update_test_Prod_Layer = "UPAA_Update_test_Prod_Layer"
    arcpy.management.MakeFeatureLayer(in_features=UPAA_Prod, out_layer=UPAA_Update_test_Prod_Layer, where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;CITY CITY VISIBLE NONE;created_user created_user VISIBLE NONE;created_date created_date VISIBLE NONE;last_edited_user last_edited_user VISIBLE NONE;last_edited_date last_edited_date VISIBLE NONE;ACRES ACRES VISIBLE NONE;LABEL LABEL VISIBLE NONE;YEAR YEAR VISIBLE NONE;LINK LINK VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")

    # Select All Cities, except Portland, By Attributte
    UPAA_Update_test_1_2_, Count_2_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=UPAA_Update_test_Prod_Layer, selection_type="NEW_SELECTION", where_clause="LABEL = 'City' And CITY <> 'PORTLAND'", invert_where_clause="")

    # Delete Selected City Rows
    Updated_Input_With_Rows_Removed_2_ = arcpy.management.DeleteRows(in_rows=UPAA_Update_test_1_2_)[0]

    # Select All NEW Cities, except Portland, Layer By Attribute
    if Updated_Input_With_Rows_Removed_2_:
        distribution_BOUNDARY_cities_2_, Count_5_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Cities, selection_type="NEW_SELECTION", where_clause="JURNAME <> 'Portland'", invert_where_clause="")

    # Append NEW City Boundaries to Production UPAA
    if Updated_Input_With_Rows_Removed_2_:
        UPAA_Update_test_Prod_Layer_2_ = arcpy.management.Append(inputs=[distribution_BOUNDARY_cities_2_], target=Updated_Input_With_Rows_Removed_2_, schema_type="NO_TEST", field_mapping="CITY \"CITY\" true true false 20 Text 0 0,First,#,distribution.BOUNDARY.cities,JURNAME,0,255;created_user \"created_user\" true true false 255 Text 0 0,First,#;created_date \"created_date\" true true false 8 Date 0 0,First,#;last_edited_user \"last_edited_user\" true true false 255 Text 0 0,First,#;last_edited_date \"last_edited_date\" true true false 8 Date 0 0,First,#;ACRES \"ACRES\" true true false 8 Double 0 0,First,#,C:\\Users\\josephh\\AppData\\Local\\Temp\\ArcGISProTemp14392\\e512dbec3ffe96b0487dfceef062ced5.sde\\distribution.BOUNDARY.cities,ACRES,-1,-1;LABEL \"LABEL\" true true false 10 Text 0 0,First,#;YEAR \"YEAR\" true true false 2 Short 0 0,First,#;LINK \"LINK\" true true false 500 Text 0 0,First,#", subtype="", expression="")[0]

    # Select Appended Cities Layer By Attribute
    if Updated_Input_With_Rows_Removed_2_:
        UPAA_Update_test_1_5_, Count_3_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=UPAA_Update_test_Prod_Layer_2_, selection_type="NEW_SELECTION", where_clause="LABEL IS NULL", invert_where_clause="")

    # Calculate Field - Capatalize City Names
    if Updated_Input_With_Rows_Removed_2_:
        UPAA_Update_test_1_6_ = arcpy.management.CalculateField(in_table=UPAA_Update_test_1_5_, field="CITY", expression="!CITY!.upper()", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Calculate Field - Add City Label
    if Updated_Input_With_Rows_Removed_2_:
        UPAA_Update_test_1_8_ = arcpy.management.CalculateField(in_table=UPAA_Update_test_1_6_, field="LABEL", expression="\"City\"", expression_type="PYTHON3", code_block="""

""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Calculate Year Field to current Year
    if Updated_Input_With_Rows_Removed_2_:
        UPAA_Update_test_1_7_ = arcpy.management.CalculateField(in_table=UPAA_Update_test_1_8_, field="YEAR", expression="time.strftime('%Y')", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Calculate Field - Add UPAA Website URL
    if Updated_Input_With_Rows_Removed_2_:
        UPAA_Update_test_1_10_ = arcpy.management.CalculateField(in_table=UPAA_Update_test_1_7_, field="LINK", expression="\"https://www.co.washington.or.us/LUT/Divisions/LongRangePlanning/Publications/index.cfm\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Calculate Acres Field
    if Updated_Input_With_Rows_Removed_2_:
        UPAA_Update_test_1_9_ = arcpy.management.CalculateField(in_table=UPAA_Update_test_1_10_, field="ACRES", expression="!Shape_Area!/43560", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Clear Selection
    if Updated_Input_With_Rows_Removed_2_:
        FG_Update1_Layer3, Count_4_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=UPAA_Update_test_1_9_, selection_type="CLEAR_SELECTION", where_clause="", invert_where_clause="")

    # Make Dist Feature Layer
    UPAA_Update_test_2_Layer2 = "UPAA_Update_test_Dist_Layer"
    arcpy.management.MakeFeatureLayer(in_features=UPAA_Dist, out_layer=UPAA_Update_test_2_Layer2, where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;CITY CITY VISIBLE NONE;created_user created_user VISIBLE NONE;created_date created_date VISIBLE NONE;last_edited_user last_edited_user VISIBLE NONE;last_edited_date last_edited_date VISIBLE NONE;ACRES ACRES VISIBLE NONE;LABEL LABEL VISIBLE NONE;YEAR YEAR VISIBLE NONE;LINK LINK VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")

    # Truncate UPAA Distribution Table
    Truncated_Table = arcpy.management.TruncateTable(in_table=UPAA_Update_test_2_Layer2)[0]

    # Append New UPAA Table to Dist
    if UPAA_Update_test_2_Layer2 and Updated_Input_With_Rows_Removed_2_:
        UPAA_Update_test_1_3_ = arcpy.management.Append(inputs=[FG_Update1_Layer3], target=Truncated_Table, schema_type="TEST", field_mapping="", subtype="", expression="")[0]

    # Integrate any little bits
    if UPAA_Update_test_2_Layer2 and Updated_Input_With_Rows_Removed_2_:
        with arcpy.EnvManager(XYTolerance="1 Feet"):
            Updated_Input_Features = arcpy.management.Integrate(in_features=[[UPAA_Update_test_1_3_, ""]], cluster_tolerance="")[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"J:\Workgroups\GISPlanning\GIS\GIS_Data_Updates_Pro\LUD_Edits.gdb", workspace=r"J:\Workgroups\GISPlanning\GIS\GIS_Data_Updates_Pro\LUD_Edits.gdb"):
        SDEUPAAwCity(*argv[1:])
