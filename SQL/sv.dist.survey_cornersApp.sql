/*
---------------------------------------------------------------------------
# NAME: sv.dist.survey_cornersApp.sql
# Description: query for spalial view using the versioned "evw0" table.
               also uses AS svcorner variable. use notpad find replace
               to replace existing table with "evw0."
# Purpose: create spatial view using tables from psqlapp1 and corners 
           feature class on distribution.
# Author:      Joe Hayes
# Updated:     2022-11-10
# Copyright:   Joe Hayes WashCo Survey

#### this code was replace with code below on 2022-11-10 ####
SELECT  survey.CORNERS_evw0.Shape, survey.V_cornersApp.CORNER_ID, survey.V_cornersApp.GPS_ID, survey.V_cornersApp.BOOK_PAGE_ENTRY, survey.V_cornersApp.DESCRIPTION, survey.V_cornersApp.STATUSDATE, survey.V_cornersApp.BLMNO, survey.V_cornersApp.Photo_name, survey.CORNERS_evw0.OBJECTID
FROM    survey.CORNERS_evw0 INNER JOIN
           survey.V_cornersApp ON survey.CORNERS_evw0.CORNER_ID = survey.V_cornersApp.CORNER_ID
---------------------------------------------------------------------------
*/

SELECT  svcorn.Shape, survey.V_cornersApp.CORNER_ID, survey.V_cornersApp.GPS_ID, survey.V_cornersApp.BOOK_PAGE_ENTRY, survey.V_cornersApp.DESCRIPTION, survey.V_cornersApp.STATUSDATE, survey.V_cornersApp.BLMNO, survey.V_cornersApp.Photo_name, svcorn.OBJECTID
FROM    survey.CORNERS_evw0 AS svcorn INNER JOIN
           survey.V_cornersApp ON svcorn.CORNER_ID = survey.V_cornersApp.CORNER_ID