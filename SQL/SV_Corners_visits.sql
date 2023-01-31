SELECT  svcorn.OBJECTID, svcorn.CORNER_ID, survey.V_CORNER_VISITS.CORNERID, survey.V_CORNER_VISITS.TheDate, survey.V_CORNER_VISITS.Status, 
        survey.V_CORNER_VISITS.ReferenceNE, survey.V_CORNER_VISITS.ReferenceSE, survey.V_CORNER_VISITS.ReferenceSW, survey.V_CORNER_VISITS.ReferenceNW, 
        survey.V_CORNER_VISITS.NewBT, survey.V_CORNER_VISITS.Staff, survey.V_CORNER_VISITS.Location, survey.V_CORNER_VISITS.Gen_Location, 
        survey.V_CORNER_VISITS.Note, svcorn.Shape
FROM    survey.CORNERS_evw0 AS svcorn INNER JOIN
           survey.V_CORNER_VISITS ON svcorn.CORNER_ID = survey.V_CORNER_VISITS.CORNERID