/*
---------------------------------------------------------------------------
# NAME: sv.dist.survey.sv_survey_gps.sql
# Description: dynamic survey_gps layer linking to   
# Author:      Joe Hayes
# Updated:     2022-11-10
# Copyright:   Joe Hayes WashCo Survey
---------------------------------------------------------------------------
*/


SELECT  survey.CORNERS.OBJECTID, ps_gps.ID, ps_gps.update_date, ps_gps.cornerID, ps_gps.GPS_ID, ps_gps.year_adj, ps_gps.northing_m, ps_gps.easting_m, ps_gps.northing_f, ps_gps.easting_f, ps_gps.notes, survey.CORNERS.Shape
FROM    Production.survey.V_GPS AS ps_gps LEFT OUTER JOIN
           survey.CORNERS ON ps_gps.cornerID = survey.CORNERS.CORNER_ID

