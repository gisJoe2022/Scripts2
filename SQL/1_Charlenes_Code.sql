/*
---------------------------------------------------------------------------
# NAME: 1_Charlenes_Code.sql
# Description: changes field character limit and type
# Purpose: 
# Author:      Charlene B.
# Updated:     2023-04-25
# Updated by:  Joe Hayes
---------------------------------------------------------------------------
*/

/* Remove duplicate CornerID records */
WITH CTE AS(
SELECT [cornerid],
RN = ROW_NUMBER()OVER(PARTITION BY cornerid ORDER BY cornerid)
FROM dbo.corner_image
)
DELETE FROM CTE WHERE RN > 1

select object_name(object_id),* from sys.key_constraints where object_name(parent_object_id) = 'Corner_Image'

-----------------------------------------------

ALTER TABLE Corner_Image
DROP CONSTRAINT PK_Corner_Image

/* Changes the field type and legnth */
ALTER TABLE Corner_Image alter column [Filename] varchar(25) NOT NULL;

/*  */
ALTER TABLE Corner_Image
ADD CONSTRAINT PK_Corner_Image PRIMARY KEY (Cornerid, Filename)

-----------------------------------------------

update corner_image
set filename = [cornerid] + 'p.pdf'


select * from Corner_Image
