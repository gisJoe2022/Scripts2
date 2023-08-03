/* 
create a view on TSQLGIS1 from PSQLAPP1.Survey.dbo.Plat_Image_Test4
and saves it AS Plat_Image_Test4

run query from the destination DB.

 */

SELECT ID, Platname, Filename, imagepath
FROM   PSQLAPP1.Survey.dbo.Plat_Image_Test4 AS Plat_Image_Test4