/*
---------------------------------------------------------------------------
# NAME: Field_Legnth_change.sql
# Description: changes field character limit and type
# Purpose: 
# Author:      Charlene B.
# Updated:     2023-04-25
# Updated by:  Joe Hayes
---------------------------------------------------------------------------
*/

ALTER TABLE Corner_Photo alter column [Photo_name] varchar(25) NOT NULL;