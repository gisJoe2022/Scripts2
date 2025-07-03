# coding=utf-8
# -------------------------------------------------------------------------------
"""
Name:           Population Estimate Tool
Purpose:        Calculate population estimates using area input

Description:    The tool uses residentially coded tax lots to select address points
                as a proxy for households. It then uses the current ACS average
                household size to estimate population.

Author:         alexat, Washington County 2018

Created:        2021-12-03
Updated:		2021-12-03 JH
"""
# -------------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import math

# """
# Define input parameters
# Area of analysis (default is Washington County boundary)
pop_area = arcpy.GetParameterAsText(0)
# Workspace, folder
ws = arcpy.GetParameterAsText(1)
# Optional: buffer distance from analysis area
buffer_dist = arcpy.GetParameterAsText(2)

# Environment settings
arcpy.env.overwriteOutput = True
arcpy.env.workspace = ws

# Define global variables
# master taxlots geometry joined to table with owner attributes
taxlots = r'Database Connections\psqlgis1_distribution_1PUBLIC.sde\distribution.TAXLOTS.tax_shapef_view'
# field containing property codes, type=text and length=3
prop_code_field = 'PROP_CODE'
# property codes for residential uses
prop_code_res = ('000','101', '102', '109', '401', '701', '707', '781')

# master address points, represent households
#Address points fc created to provide a more accurate representation of # of dwellings
#address_pts = r'Database Connections\washsde_distribution_sde_public.sde\distribution.ADDRESS.core_situs_address'
address_pts = r'Database Connections\psqlgis1_production_CENSUS.sde\production.CENSUS.PopEmp_Estimates'
# ACS 5-year population estimates
acs_5yr_tracts = r'\\Emcgis\nas\GISDATA\Workgroups\GISPlanning\GIS\DATA\Census\ACS_2018_5yr\ACS_2018_5yr.gdb\Tracts_2018_5yr_ACS_pop_hu_moepct'
acs_field = 'Pop_per_HU'
acs_fields = ('FIPS2', 'Pop_per_HU')
pop_field = 'pop_est'

# Define functions
def roundup( a, digits=0 ):
	"""
	round input number up to specified digits
	source: https://www.w3resource.com/python-exercises/math/python-math-exercise-69.php
	"""
	n = 10 ** -digits
	return round(math.ceil(a / n) * n, digits)


def make_hh_lyr():
	"""
	Select points that fall within residential taxlots. Create a new layer from selection.
	"""

	hh_selection = arcpy.SelectLayerByLocation_management(address_lyr, overlap_type='INTERSECT',
	                                                      select_features=taxlot_lyr, selection_type="NEW_SELECTION")
	hh_lyr = arcpy.MakeFeatureLayer_management(hh_selection, 'Residential Addresses')

	return hh_lyr


def select_by_analysis_area( input_tracts_lyr, input_taxlot_lyr, input_hh_lyr, dist=None ):
	"""
	Select addresses that fall within the area of interest.
	Default is the County boundary, when no polygon is specified.
	"""
	acs_pop_area_select = arcpy.SelectLayerByLocation_management(input_tracts_lyr, overlap_type='INTERSECT',
	                                                             select_features=analysis_area_lyr,
	                                                             search_distance=dist,
	                                                             selection_type='NEW_SELECTION')

	taxlots_select = arcpy.SelectLayerByLocation_management(input_taxlot_lyr, overlap_type='INTERSECT',
	                                                        select_features=analysis_area_lyr,
	                                                        search_distance=dist,
	                                                        selection_type='NEW_SELECTION')

	hh_pop_area = arcpy.SelectLayerByLocation_management(input_hh_lyr,
	                                                     overlap_type='INTERSECT',
	                                                     select_features=analysis_area_lyr,
	                                                     selection_type='NEW_SELECTION')

	acs_pop_area_lyr = arcpy.MakeFeatureLayer_management(acs_pop_area_select, 'ACS 5yr Tracts10 in Analysis Area')
	taxlots_pop_area_lyr = arcpy.MakeFeatureLayer_management(taxlots_select, 'Taxlots_in_Analysis_Area')
	hh_pop_area_lyr = arcpy.MakeFeatureLayer_management(hh_pop_area, 'Households_in_Analysis_Area')

	return acs_pop_area_lyr, taxlots_pop_area_lyr, hh_pop_area_lyr


def average_acs_hh( select_tract_lyr, gdb ):
	"""
	Calculate average household size from ACS data for the input area.
	"""
	tracts = select_tract_lyr
	output_gdb = gdb
	out_tbl = output_gdb + '\\' + 'ave_hh_tbl'
	tracts_tbl = arcpy.MakeTableView_management(tracts, 'Tracts Table')
	#
	ave_hh_stats = arcpy.Statistics_analysis(tracts_tbl, out_tbl, statistics_fields="Pop_per_HU MEAN")




	averages = arcpy.SearchCursor(ave_hh_stats, fields='MEAN_Pop_per_HU')

	for average in averages:
		ave = average.MEAN_Pop_per_HU

	# return math.ceil(ave)
	return out_tbl, ave


def calc_pop( ave_co_hh, calc_hh_lyr ):
	"""
	Get count of households and calculate population estimate
	by multiplying households by average household size.
	"""
	hh_tbl = arcpy.MakeTableView_management(calc_hh_lyr, 'Selected Addresses Table')
	# count households
	hh_count_result = arcpy.GetCount_management(hh_tbl)
	# return string containing the command/count output
	hh_count = hh_count_result.getOutput(0)
	# convert string count to a float and calculate pop
	pop_est = ave_co_hh * float(unicode(hh_count))

	return hh_count, pop_est


def create_output_ws( out_location ):
	"""
	Save layer files to project folder.
	"""
	out_folder2 = ws + '\\' + out_location
	if not os.path.exists(out_folder2):
		print('creating output folder: {}'.format(out_location))
		os.makedirs(out_folder2)
	out_gdb = out_folder2 + '\\' + out_location + '.gdb'
	if not os.path.exists(out_gdb):
		print('creating output geodatabase: {}.gdb'.format(out_location))
		arcpy.CreateFileGDB_management(out_folder2, out_location + '.gdb')

	# arcpy.SaveToLayerFile_management(in_lyr, out_folder2 + '\\' + out_name)

	return out_folder2, out_gdb


def ave_hh_by_tract():
	# TODO: calculate hh average and population for each tract
	# Make search cursor to loop through tracts
	with arcpy.da.SearchCursor(acs_tracts_lyr, [ 'OID@', acs_field ]) as tract_cursor:
		for tract in tract_cursor:
			acs_query = 'OBJECTID = {}'.format(int(tract[ 0 ]))
			arcpy.SelectLayerByAttribute_management(acs_tracts_lyr, 'NEW_SELECTION', acs_query)
			arcpy.SelectLayerByLocation_management(hh_lyr, 'INTERSECT', acs_tracts_lyr, selection_type='NEW_SELECTION')

			results, ave_hh = average_acs_hh(acs_tracts_lyr, working_gdb)
			pop = calc_pop(ave_hh, hh_lyr)

		# Calculate fields with OID, ave_hh, hh, and pop


name = os.path.basename(pop_area)
test_folder = 'Population_Estimate_' + name
# working_gdb = ws + '\\' + test_folder + '\\' + test_folder + '.gdb'

# Process
# 1. Set-up Data
# ---------------------------------------------------------------------
# Create Feature Layers for geoprocessing
# ---------------------------------------------------------------------
# residential taxlots layer
taxlot_lyr = arcpy.MakeFeatureLayer_management(taxlots, 'Residential Taxlots',
                                               prop_code_field + ' IN ' + str(prop_code_res))
# address points layer
address_lyr = arcpy.MakeFeatureLayer_management(address_pts, 'Address Points')
#Select only housing points
arcpy.SelectLayerByAttribute_management (in_layer_or_view="Address Points", selection_type="NEW_SELECTION", where_clause="AveHHsize > 0")

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "production.CENSUS.PopEmp_Estimates"
#arcpy.SelectLayerByAttribute_management(in_layer_or_view="production.CENSUS.PopEmp_Estimates", selection_type="NEW_SELECTION", where_clause="AveHHsize > 0")

# residential households layer
hh_lyr = make_hh_lyr()
# area of analysis layer
analysis_area_lyr = arcpy.MakeFeatureLayer_management(pop_area, 'Area of Analysis')
# ACS tracts layer
acs_tracts_lyr = arcpy.MakeFeatureLayer_management(acs_5yr_tracts, 'ACS 5yr Tracts10 Household')

# 2. Select Data
# -----------------------------------------------------------------------
# Select tracts, residential taxlots, and address points that fall
# within the analysis area
# -----------------------------------------------------------------------

tracts_select, taxlots_select, hh_select = select_by_analysis_area(acs_tracts_lyr, taxlot_lyr, hh_lyr, buffer_dist)

# 3. Save Data
# -----------------------------------------------------------------------
# if not already existing, create working folder and geodatabase
# if true, save selected taxlots and/or address points
# -----------------------------------------------------------------------

working_folder, working_gdb = create_output_ws(test_folder)

# copy selected taxlots and/or households to working gdb

arcpy.CopyFeatures_management (taxlots_select, working_gdb + '\\' + 'taxlots')

arcpy.CopyFeatures_management (hh_select, working_gdb + '\\' + 'households')

# 4. Calculate Average Household Size
# -----------------------------------------------------------------------
# Calculate from tracts the average household size for the analysis area
# -----------------------------------------------------------------------

results_tbl, ave_hh = average_acs_hh(tracts_select, working_gdb)

# 5. Calculate Population Estimate
# -----------------------------------------------------------------------
# Calculate population estimate by multiplying average household by count
# of households
# -----------------------------------------------------------------------

households, population = calc_pop(ave_hh, hh_select)

# 6. Report Results
# -----------------------------------------------------------------------
# Save calculations to table. Add message to geoprocessing window with
# calculation results: number of households, average household size,
# and estimated population
# -----------------------------------------------------------------------
# List of fields to add, all with same type, precision, and scale
fields = [ 'hh_count', 'pop_est' ]

# list comprehension to add multiple fields
[ arcpy.AddField_management(results_tbl, field_name, "LONG") for field_name in fields ]
# add values to table for number of households and population estimate
arcpy.CalculateField_management(results_tbl, fields[ 0 ], households)
arcpy.CalculateField_management(results_tbl, fields[ 1 ], population)

arcpy.AddMessage('Average household size: ' + str(roundup(ave_hh, 2)))
arcpy.AddMessage('Number of households: ' + str(int(households)))
arcpy.AddMessage('Estimated population: ' + str(int(population)))
