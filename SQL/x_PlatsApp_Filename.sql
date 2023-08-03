/*
---------------------------------------------------------------------------
# NAME:        x_PlatsApp_Filename.sql
# Description: v_PlatsApp with filename added
# Purpose:     resource for reformatting the plat image records
# Author:      Joe Hayes
# Updated:     05-09-2023
# Updated by:  Joe Hayes
---------------------------------------------------------------------------
*/

SELECT TOP (100) PERCENT dbo.Plat_Main.Platname AS [Plat Name], dbo.Plat_Main.[Book/Page], dbo.Plat_Main.Received AS [Received Date], dbo.Plat_Main.Recorded AS [Recorded Date], dbo.Plat_Image.Filename, dbo.Plat_Main.DocNumber AS [Doc Number], dbo.Plat_Main.BusinessName, dbo.Plat_Main.Declarant, 
           dbo.CityCode.CityName AS City, dbo.Surveyors.SurveyorName AS Surveyor, dbo.Plat_Main.Surveyornumber AS [Surveyor's Number'], dbo.Plat_Main.Reserved
FROM   dbo.Plat_Main INNER JOIN
           dbo.Plat_Image ON dbo.Plat_Main.Platname = dbo.Plat_Image.Platname LEFT OUTER JOIN
           dbo.CityCode ON dbo.Plat_Main.City = dbo.CityCode.CityCode LEFT OUTER JOIN
           dbo.Surveyors ON dbo.Plat_Main.Surveyornumber = dbo.Surveyors.SurveyorNumber
WHERE (dbo.Plat_Main.Reserved = 0)