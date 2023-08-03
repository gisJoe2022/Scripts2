/*
---------------------------------------------------------------------------
# NAME: dbo.Plat_Image_fielname.sql
# Description: create new plat image table with addtional info
# Purpose:     image rename testing
# Author:      Joe Hayes
# Updated:     2023-05-30
---------------------------------------------------------------------------
*/


SELECT   TOP (100) PERCENT dbo.Plat_Main.Platname AS [Plat Name], dbo.Plat_Main.[Book/Page], dbo.Plat_Image.Filename, dbo.Plat_Main.Recorded AS [Recorded Date], dbo.Plat_Main.Received AS [Received Date], dbo.Plat_Main.DocNumber AS [Doc Number], dbo.Plat_Main.BusinessName, dbo.Plat_Main.Declarant, dbo.CityCode.CityName AS City, dbo.Surveyors.SurveyorName AS Surveyor, dbo.Plat_Main.Surveyornumber AS [Surveyor's Number'], dbo.Plat_Main.Reserved
/* into = name if new table */
into Plat_Image_filename
FROM     dbo.Plat_Main INNER JOIN
          dbo.Plat_Image ON dbo.Plat_Main.Platname = dbo.Plat_Image.Platname LEFT OUTER JOIN
          dbo.CityCode ON dbo.Plat_Main.City = dbo.CityCode.CityCode LEFT OUTER JOIN
          dbo.Surveyors ON dbo.Plat_Main.Surveyornumber = dbo.Surveyors.SurveyorNumber
WHERE   (dbo.Plat_Main.Reserved = 0)