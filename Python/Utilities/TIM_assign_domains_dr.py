# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# TIM_assign_domains.py v1.0

# Created on: 3/20/2020 while working from home during the COVID-19 Pandemic

# Author: Joe Hayes

# Description: Assign coded value domains to a TIM point or line features class.
#              Comment out fields that don't need updating.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Local variables:
prod_tim_points = "Database Connections\\washsde_production_transpor.sde\\production.TRANSPOR.TIM_points"

# assign coded value domain to field

# # Status
# print('Adding Status Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="Status_0", domain_name="GAP_Status", subtype_code="")
# print('Complete')
# print('')

# # Source
# print('Adding Source Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="Source_1", domain_name="GAP_Source2_1", subtype_code="")
# print('Complete')
# print('')

# # Need Type 
# print('Adding Need Type Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="nType_1", domain_name="GAP_nType2_1", subtype_code="")
# print('Complete')
# print('')

# # For Public 
# print('Adding For Public Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="forPub_1", domain_name="GAP_YES_NO_UN", subtype_code="")
# print('Complete')
# print('')

# # Fclass 
# print('Adding Fclass Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="Fclass_1", domain_name="GAP_Fclass", subtype_code="")
# print('Complete')
# print('')

# # URMD 
# print('Adding URMD Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="URMD_1", domain_name="GAP_YES_NO_UN", subtype_code="")
# print('Complete')
# print('')

# # County Road
# print('Adding County Road Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="CntyRd_1", domain_name="GAP_YES_NO_UN", subtype_code="")
# print('Complete')
# print('')

# # TDT
# print('Adding TDT Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="TDT_1", domain_name="GAP_YES_NO_UN", subtype_code="")
# print('Complete')
# print('')

# # Multi-Jur
# print('Adding Multi-Jur Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="multiJur_1", domain_name="GAP_YES_NO_UN", subtype_code="")
# print('Complete')
# print('')

# # Need Catagory
# print('Adding Nedd Catagory Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="nCat_2", domain_name="GAP_nCAT3_1", subtype_code="")
# print('Complete')
# print('')

# # List 1
# print('Adding List 1 Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="TIM3_List1", domain_name="GAP_fSource_1", subtype_code="")
# print('Complete')
# print('')

# # List 2
# print('Adding List 2 Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="TIM3_List2", domain_name="GAP_fSource_1", subtype_code="")
# print('Complete')
# print('')

# # List 3
# print('Adding List 3 Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="TIM3_List3", domain_name="GAP_fSource_1", subtype_code="")
# print('Complete')
# print('')

# # List 4
# print('Adding List 4 Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="TIM3_List4", domain_name="GAP_fSource_1", subtype_code="")
# print('Complete')
# print('')

# # List 5
# print('Adding List 5 Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="TIM3_List5", domain_name="GAP_fSource_1", subtype_code="")
# print('Complete')
# print('')

# # List 6
# print('Adding List 6 Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="TIM3_List6", domain_name="GAP_fSource_1", subtype_code="")
# print('Complete')
# print('')

# # Funding Source 1
# print('Adding Funding Source 1 Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="AFsource1_3", domain_name="GAP_fSource_1", subtype_code="")
# print('Complete')
# print('')

# # Funding Source 2
# print('Adding Funding Source 2 Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="AFsource2_3", domain_name="GAP_fSource_1", subtype_code="")
# print('Complete')
# print('')

# # Funding Source 3
# print('Adding Funding Source 3 Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="AFsource3_3", domain_name="GAP_fSource_1", subtype_code="")
# print('Complete')
# print('')

# # Project Time Frame
# print('Adding Project Time Frame Domain')
# arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="projPeriod_3", domain_name="GAP_projPeriod2", subtype_code="")
# print('Complete')
# print('')

# Commissioner District
print('Adding Commissioner District Domain')
arcpy.AssignDomainToField_management(in_table="Database Connections/washsde_production_transpor.sde/production.TRANSPOR.TIM_points", field_name="comDist_1", domain_name="GAP_comDist_1", subtype_code="")
print('Complete')
print('')

print("Have a Nice Day")