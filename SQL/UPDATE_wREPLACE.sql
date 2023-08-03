/*
---------------------------------------------------------------------------
# NAME: UPDATE_wREPLACE.sql
# Description: instantly replaces special characters.
# Purpose: Batch data clean-up.
# Author:      Joe Hayes
# Updated:     2023-04-13
---------------------------------------------------------------------------
*/

UPDATE 
    dbo.x_Test_CoRoads_IMG
SET 
    File_name = REPLACE(File_name,'-','_')
WHERE 
    File_name LIKE '%-%'