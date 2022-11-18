
//hospital/urgent care customn pop
{Name}

//large grocery stores custom pop
{NAME}

//elemmetary schools custom pop
{Institution_Name_Line1}


//Rail Station custom pop
{STATION} {TYPE} Station

//Bus Weekday offs custom pop
{WKDYOFFS} weekly offs at {PUBLICSTOP}.

//Bus Weekday ons custom pop
{WKDYONS} weekly ons at {PUBLICSTOP}.

//city custom pop
City of {CITYNAME}

//POINTS - completed mstip custom pop
<div style="padding: 5px; background-color: rgb(170, 102, 205);"><b style=""><font color="#ffffff" face="Tahoma" size="3" style="">{projName_4}</font></b></div><p style="margin: 0in;"><font size="2"><font face="Tahoma" style=""><span style="font-weight: bold;">Street: </span></font><font face="Tahoma" style="">{expression/expr1}</font><font face="Tahoma" style=""><span style="font-weight: bold;"><br />Location: </span></font><span style="font-family: Tahoma;">{expression/expr2}</span><font face="Tahoma" style=""><span style="font-weight: bold;"><br />Improvements: </span></font><font face="Tahoma" style="">{expression/expr0}</font></font></p><p style="margin: 0in;"><font size="2"><font face="Tahoma"><span style="font-weight: bold;">Construction Start:</span> </font><span style="font-family: Tahoma;">{expression/expr4}<br /></span><font face="Tahoma"><span style="font-weight: bold;">Complete: </span></font><span style="font-family: Tahoma;">{expression/expr5}</span><br /></font></p><font face="Tahoma" size="2"><span style="font-weight: bold;">Funding Source: </span>{AFsource1_3} {AFsource2_3} {AFsource3_3}<br /></font><p style="margin: 0in;"><font size="2"><font face="Tahoma"><span style="font-weight: bold;">Cost Estimate: </span></font><span style="font-family: Tahoma;">{expression/expr6}</span><font face="Tahoma"><span style="font-weight: bold;"><br />Final Cost:</span> </font><span style="font-family: Tahoma;">{expression/expr7}</span></font></p><p style="margin: 0in;"><font face="Tahoma" size="2"><span style="font-weight: bold;">Type: </span>{nType_1}<span style="font-weight: bold;"></span></font></p><p style="margin: 0in;"><font face="Tahoma" size="2"><span style="font-weight: bold;">Category: </span>{nCat_2}<br /><span style="font-weight: bold;">Com. District: </span>{comDist_1}</font></p>

//LINES - completed mstip custom pop
<div style="padding: 5px; background-color: rgb(170, 102, 205);"><b style=""><font color="#ffffff" face="Tahoma" size="3" style="">{projName_4}</font></b></div><p style="margin: 0in;"><font size="2"><font face="Tahoma"><span style="font-weight: bold;">Street: </span></font><font face="Tahoma">{expression/expr1}</font><font face="Tahoma"><span style="font-weight: bold;"><br />From: </span></font><span style="font-family: Tahoma;">{expression/expr3}<br /></span></font><font face="Tahoma" style="font-size: small;"><span style="font-weight: bold;">To: </span></font><span style="font-size: small; font-family: Tahoma;">{expression/expr2}</span><font size="2"><font face="Tahoma"><span style="font-weight: bold;"><br />Improvements: </span></font><font face="Tahoma">{expression/expr0}</font></font></p><p style="margin: 0in;"><font size="2"><font face="Tahoma"><span style="font-weight: bold;">Construction Start:</span> </font><span style="font-family: Tahoma;">{expression/expr4}<br /></span><font face="Tahoma"><span style="font-weight: bold;">Complete: </span></font><span style="font-family: Tahoma;">{expression/expr5}</span><br /></font></p><font face="Tahoma" size="2"><span style="font-weight: bold;">Funding Source: </span>{AFsource1_3} {AFsource2_3} {AFsource3_3}<br /></font><p style="margin: 0in;"><font size="2"><font face="Tahoma"><span style="font-weight: bold;">Cost Estimate: </span></font><span style="font-family: Tahoma;">{expression/expr6}</span><font face="Tahoma"><span style="font-weight: bold;"><br />Final Cost:</span> </font><span style="font-family: Tahoma;">{expression/expr7}</span></font></p><p style="margin: 0in;"><font face="Tahoma" size="2"><span style="font-weight: bold;">Type: </span>{nType_1}<span style="font-weight: bold;"></span></font></p><p style="margin: 0in;"><font face="Tahoma"><font size="2"><span style="font-weight: bold;">Category: </span>{nCat_2}<br /><span style="font-weight: bold;">Com. District: </span>{comDist_1}</font></font></p>

//pimp nd
IIf (IsEmpty($feature["PIMP_2"]), 'No Data', $feature["PIMP_2"]);

//street nd
IIf (IsEmpty($feature["stName_1"]), 'No Data', $feature["stName_1"]);

//from st nd
IIf (IsEmpty($feature["fromST_1"]), 'No Data', $feature["fromST_1"]);

//to st nd
IIf (IsEmpty($feature["toST_1"]), 'No Data', $feature["toST_1"]);

//const start data nd
IIf(IsEmpty($feature["projConStartDate_4"]), 'No Data', Text($feature["projConStartDate_4"], 'M/d/Y'));

//Complete Date nd
IIf(IsEmpty($feature["compDate_5"]), 'No Data', Text($feature["compDate_5"], 'M/d/Y'));

//cost estimate nd
IIf(IsEmpty($feature["costEst_4"]), Text('No Data'), Text($feature["costEst_4"], '$###,###,###,###'));

//final cost nd
IIf(IsEmpty($feature["finalCost_5"]), Text('No Data'), Text($feature["finalCost_5"], '$###,###,###,###'));

//rtp fin constrained - configure popup
<b><font color="#ffffff" size="3" style="background-color: rgb(137, 205, 102);"> {Workspace} </font></b><br /><b>Description</b>: {Descriptio}.

//rtp fine constrained roads - primar upper
Upper($feature["Primary_Pu"])

//rtp fine constrained roads - secondary upper
Upper($feature.Secondary)

//lane number defic custom pop
Planned: {Lanes}
Existing: {xLanes} Lanes

// candiate projects popup
Cost Estimate: ${costEst_4}
Commissioner District: {comDist_1}

Project Description: {PIMP_2}