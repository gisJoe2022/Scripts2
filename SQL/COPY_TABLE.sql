/*
---------------------------------------------------------------------------
# NAME: COPY_TABLE.sql
# Description: create a copy of an existing table
# Purpose:     testing prior to change to authoratative data
# Author:      Joe Hayes
# Updated:     2023-05-24
---------------------------------------------------------------------------
*/

/* selects all the records from an existing table and inserts them into
   the new table */
select *
into Plat_Image_Test3
from dbo.Plat_image