/* 
---------------------------------------------------------------------------
# NAME:     SQL_Date_Ranges.sql 
# Desc:     ArcGIS Pro SQL definition query. 
# Purpose:  Auto updates Corner Status maps years classes using YEAR(GETDATE())
# Author:   Joe Hayes
# Created:  8/30/2023
# Updated:  8/31/2023
 ---------------------------------------------------------------------------
 */


/* 5 years or less */
/* switching the definition query option out of SQL view will change the query  */
(Final_Year >= YEAR(GETDATE()) -5) AND (AltMon IN ('NCC', 'GLO') OR AltMon IS NULL)

/* 6-10 years */
/* switching the definition query option out of SQL view will change the query  */
(Final_Year <= YEAR(GETDATE()) -6) AND Final_Year >=( YEAR(GETDATE()) -10) AND (AltMon IN ('NCC', 'GLO') OR AltMon IS NULL)

/* 11-20 years */
/* switching the definition query option out of SQL view will change the query  */
(Final_Year <= YEAR(GETDATE()) -11) AND Final_Year >=( YEAR(GETDATE()) -20) AND (AltMon IN ('GLO', 'NCC') OR AltMon is NULL)

 /* 21-35 years */
/* switching the definition query option out of SQL view will change the query  */
(Final_Year <= YEAR(GETDATE()) -21) AND Final_Year >=( YEAR(GETDATE()) -35) AND (AltMon IN ('GLO', 'NCC') OR AltMon is NULL)

/* Greater than 35 years */
/* switching the definition query option out of SQL view will change the query  */
(Final_Year < YEAR(GETDATE()) -35) AND (AltMon IN ('GLO', 'NCC') OR AltMon is NULL)

/* No BT Entry  */
AltMon IS NULL And Final_Year IS NULL

/* Maintained by Adjacent County */
AltMon = 'OTHC'

/* Non-Controling Corner */
AltMon = 'NCC'

/* 4 Corner Stone */
AltMon = '4COR'

/* Willamette Stone */
AltMon = 'WLST'