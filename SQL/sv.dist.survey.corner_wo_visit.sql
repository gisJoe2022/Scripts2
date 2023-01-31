/*
---------------------------------------------------------------------------
# NAME: sv.dist.survey.corner_wo_visit.sql
# Description: query for spalial view using the versioned "evw0" table.
               also uses AS svcorner variable. use notpad find replace
               to replace existing table with "evw0."
# Purpose: create spatial view using tables from psqlapp1 and corners 
           feature class on distribution.
# Author:      Joe Hayes
# Updated:     2022-11-10
# Copyright:   Joe Hayes WashCo Survey

##### this code was replace with code below on 2022-11-10 ####
SELECT  survey.CORNERS.Shape, survey.CORNERS.CORNER_ID, survey.V_corner_no_visit.note, survey.CORNERS.OBJECTID
FROM    survey.CORNERS INNER JOIN
           survey.V_corner_no_visit ON survey.CORNERS.CORNER_ID = survey.V_corner_no_visit.CORNER_ID
---------------------------------------------------------------------------
*/

SELECT  svcorn.Shape, svcorn.CORNER_ID, survey.V_corner_no_visit.note, svcorn.OBJECTID
FROM    survey.CORNERS_evw AS svcorn INNER JOIN
           survey.V_corner_no_visit ON svcorn.CORNER_ID = survey.V_corner_no_visit.CORNER_ID