/*
---------------------------------------------------------------------------
# NAME: Delete_by_criteria.sql
# Description: delete only rows that meet a simple keyword criteria
# Purpose: Batch data clean-up.
# Author:      Joe Hayes
# Updated:     2023-04-13
---------------------------------------------------------------------------
*/


DELETE FROM dbo.x_Test_CoRoads_IMG WHERE File_name LIKE '%.tif%'