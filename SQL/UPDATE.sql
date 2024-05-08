/*
---------------------------------------------------------------------------
# NAME: UPDATE.sql
# Description: update one field using the values from another field and text
#              using CONCAT()
# Purpose: Batch data clean-up.
# Author:      Joe Hayes
# Updated:     2023-04-18
---------------------------------------------------------------------------
*/

UPDATE dbo.CntyRoad_Image /* table with data */
SET Filename = CONCAT('CR', CRoad_ID, '.pdf') /* filename is the field to be updated with CONCAT() */  