/*
---------------------------------------------------------------------------
# NAME: sv.dist.survey.corner_visit.sql
# Description: query for spalial view using the versioned "evw0" table.
               also uses AS svcorner variable. use notpad find replace
               to replace existing table with "evw0."
# Purpose: create spatial view using tables from psqlapp1 and corners 
           feature class on distribution.
# Author:      Joe Hayes
# Updated:     2022-11-10
# Copyright:   Joe Hayes WashCo Survey

##### this code was replace with code below on 2022-11-10 ####
SELECT  survey.CORNERS.Shape, survey.CORNERS.CORNER_ID, survey.V_CORNER_VISITS.CORNERID, survey.V_CORNER_VISITS.TheDate, survey.V_CORNER_VISITS.Status, survey.V_CORNER_VISITS.ReferenceNE, survey.V_CORNER_VISITS.ReferenceSE, survey.V_CORNER_VISITS.ReferenceSW, survey.V_CORNER_VISITS.ReferenceNW, survey.V_CORNER_VISITS.NewBT, survey.V_CORNER_VISITS.Staff, 
           survey.V_CORNER_VISITS.Location, survey.V_CORNER_VISITS.Gen_Location, survey.V_CORNER_VISITS.Note, survey.CORNERS.OBJECTID
FROM    survey.CORNERS INNER JOIN
           survey.V_CORNER_VISITS ON survey.CORNERS.CORNER_ID = survey.V_CORNER_VISITS.CORNERID
---------------------------------------------------------------------------
*/

SELECT  svcorn.Shape, svcorn.CORNER_ID, survey.V_Corners_FYear.CORNERID, svcorn.AltMon, survey.V_Corners_FYear.BT_Year, survey.V_Corners_FYear.Visit_Year, survey.V_Corners_FYear.Final_Year, svcorn.OBJECTID
FROM    survey.CORNERS_evw0 AS svcorn INNER JOIN
           survey.V_Corners_FYear ON svcorn.CORNER_ID = survey.V_Corners_FYear.CORNERID