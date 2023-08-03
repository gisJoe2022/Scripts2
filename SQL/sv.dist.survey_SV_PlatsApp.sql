


SELECT g.OBJECTID, a.Platname, a.BookPage, a.Filename, a.Recorded, a.DocNumber, a.SurveyorName, a.Surveyornumber, g.Shape
FROM   survey.PLATS_evw1 AS g INNER JOIN
           survey.v_platsapp1221 AS a ON g.PLATNAME = a.Platname