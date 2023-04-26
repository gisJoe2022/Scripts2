USE [distribution]
GO

/****** Object:  View [survey].[v_find_surveyor]    Script Date: 3/23/2023 10:59:45 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [survey].[v_find_surveyor] AS SELECT  SURVEY.survpts.SHAPE, SURVEY.survpts.SURVNUM, SURVEY.V_Surveyors.Surveytext, SURVEY.V_Surveyors.Surveyornumber FROM  SURVEY.survpts, SURVEY.V_Surveyors WHERE SURVEY.survpts.SURVNUM = SURVEY.V_Surveyors.Surveytext
GO

