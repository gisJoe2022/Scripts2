/*
---------------------------------------------------------------------------
# NAME: INSERT.sql
# Description: inserts rows from one table to another. does not alter 
#              source table.
# Purpose: Batch data import
# Author:      Joe Hayes
# Updated:     2023-04-13
---------------------------------------------------------------------------
*/

/* when field names are the same */
INSERT INTO corner_image (ID, image)
SELECT nl.ID, nl.image
FROM new_list nl

/* when field names are different */
INSERT INTO corner_image (ID, image)
SELECT nl.new_list_id, nl.new_list_image
FROM new_list nl

/* test INSERT */
INSERT INTO dbo.x_Test_CoRoads_IMG (CRoad, File_name)
SELECT cr.CRoad_ID, cr.Filename
FROM dbo.CntyRoad_Image cr