SELECT  surveypts.OBJECTID, survey.v_surveyApp.SurvNum, survey.v_surveyApp.Surveyornumber, survey.v_surveyApp.Received, survey.v_surveyApp.Filed, survey.v_surveyApp.Client, survey.v_surveyApp.SurveyorName, survey.v_surveyApp.Date_Survey, surveypts.Shape
FROM    survey.SURVEYPTS_evw AS surveypts INNER JOIN
           survey.v_surveyApp ON surveypts.SURVNUM = survey.v_surveyApp.SurvNum