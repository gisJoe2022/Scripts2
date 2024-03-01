/* 
Cast the year only from a date field to a new field called YearOnly 
in a view

ex. DATEPART(YEAR, dbo.Plat_Main.Recorded) AS YearOnly

 */

 SELECT TOP (100) PERCENT dbo.Plat_Main.Platname AS [Plat Name], dbo.Plat_Main.[Book/Page], dbo.Plat_Main.Received AS [Received Date], dbo.Plat_Main.Recorded AS [Recorded Date], dbo.Plat_Main.DocNumber AS [Doc Number], dbo.Plat_Main.BusinessName, dbo.Plat_Main.Declarant, dbo.CityCode.CityName AS City, dbo.Surveyors.SurveyorName AS Surveyor, dbo.Plat_Main.Surveyornumber AS [Surveyor's Number'], 
          dbo.Plat_Main.Reserved, DATEPART(YEAR, dbo.Plat_Main.Recorded) AS YearOnly
FROM   dbo.Plat_Main LEFT OUTER JOIN
          dbo.CityCode ON dbo.Plat_Main.City = dbo.CityCode.CityCode LEFT OUTER JOIN
          dbo.Surveyors ON dbo.Plat_Main.Surveyornumber = dbo.Surveyors.SurveyorNumber
WHERE  (dbo.Plat_Main.Reserved = 0)