/*
---------------------------------------------------------------------------
# NAME: sv.dist.survey_corners_Data.sql
# Description: query for spalial view using the versioned "evw0" table.
               also uses AS svcorner variable. use notpad find replace
               to replace existing table with "evw0."
# Purpose: create spatial view using tables from psqlapp1 and corners 
           feature class on distribution.
# Author:      Joe Hayes
# Updated:     2022-11-10
# Copyright:   Joe Hayes WashCo Survey

#### this code was replace with code below on 2022-11-10 ####
SELECT  survey.CORNERS.Shape, survey.CORNERS.CORNER_ID, survey.V_Corners_Data.CORNERID, survey.CORNERS.AltMon, survey.V_Corners_Data.TopYear, survey.CORNERS.OBJECTID
FROM    survey.CORNERS INNER JOIN
           survey.V_Corners_Data ON survey.CORNERS.CORNER_ID = survey.V_Corners_Data.CORNERID
---------------------------------------------------------------------------
*/

SELECT  svcorn.Shape, svcorn.CORNER_ID, survey.V_Corners_Data.CORNERID, svcorn.AltMon, survey.V_Corners_Data.TopYear, svcorn.OBJECTID
FROM    survey.CORNERS_evw0 AS svcorn INNER JOIN
           survey.V_Corners_Data ON svcorn.CORNER_ID = survey.V_Corners_Data.CORNERID