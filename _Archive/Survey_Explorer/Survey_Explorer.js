
// url parameters example
"https://wc34926.co.washington.or.us:3344/webappbuilder/apps/2/?query=Survey_Explorer_451,Benchmark_ID,102&showLayers=Survey_Explorer_451"

// Mt Bachelor url parameters
"https://gisims.co.washington.or.us/gis/Survey/se2/SurveyExplorer.html?query=Survey_Explorer_451,Benchmark_ID,102&showLayers=Survey_Explorer_451"


// Color Block Popup Header
<div style="padding: 5px; background-color: rgb(170, 102, 205);"><b style="">
<font color="#ffffff" face="Verdana" size="3" style="">{projName_4}</font></b></div><p style="margin: 0in;"><br /></p>
// border style
 '  <div style="padding: 5px; background-color: rgb(255, 255, 255); border: solid black;">   '


// image to PDF - taxmap example
https://pdoclsde1.co.washington.or.us/images/pdfbuilderasp/tiff2pdf.asp?doctype=taxmaps&imageto={expression/expr1}

// gecontrol link from iSpirits
javascript:sendImage('gc49_1','geocontrol')



// CORNERS -----------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------

// popup html
<div style="padding: 5px; background-color: rgb(168, 112, 0);"><b><font face="Verdana">
<font color="#ffffff" size="3" style="">Corner</font></font></b></div><p style="margin: 0in;"><font face="Tahoma"><b>ID</b>: {CORNER_ID}<br /><b>BLM Num</b>:{BLMNO}<br /><b>GPS ID</b>: {GPS_ID} <br /><b>Book/Page</b>: </font>{expression/expr5}</p><p style="margin: 0in;"><font face="Tahoma"><b>Status Date</b>: </font>{expression/expr4}<font face="Tahoma"><br /><b>Description</b>: {expression/expr0}<br /><b>Image</b>: <a href="{expression/expr1}" rel="nofollow ugc noopener noreferrer" style="" target="_blank">PDF</a><br /><b>Site Photo</b>: <a href="{expression/expr2}" rel="nofollow ugc noopener noreferrer" style="" target="_blank">PDF (if available)</a></font><br /></p>

// corner - desciption proper case
Proper($feature.DESCRIPTION, 'firstword')

// corner - image
"http://mtbachelor.co.washington.or.us/images/survey/BTBooks/" + $feature["CORNER_ID"]  +  ".pdf"

// corner - site photo
"http://mtbachelor.co.washington.or.us/images/survey/BTBOOKS/Site_Photo/" + $feature["CORNER_ID"] + ".pdf"

// boop/page - no data
if ($feature["BOOK_PAGE_ENTRY"] == '//'){
    return 'No Data'
}
return $feature["BOOK_PAGE_ENTRY"]


// corner - popup
Corners
Corner ID: {CORNER_ID}
BLM Num:{BLMNO}
GPS ID: {GPS_ID}
Book/Page: {BOOK_PAGE_ENTRY}

Status Date: {STATUSDATE}  
Description: {expression/expr0}
Image: PDF
Site Photo: PDF (if available)



// BENCHMARKS --------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------

// benchmark corlor header
<div style="padding: 5px; background-color: rgb(168, 112, 0);"><font color="#ffffff" face="Tahoma" size="3"><b>BENCHMARK</b></font></div><p style="margin: 0in;"><b>ID</b>: {Benchmark_ID}<br /><b>Elevation: </b>{Elevation1}<br /><b>Monument: </b>{expression/expr1}<br /><b>Established</b>: {Date_Established}<br /><b>Stamping</b>: {expression/expr0}<br /><b>Reference 1</b>: {expression/expr2}<br /><b>Reference 2</b>: {expression/expr3}<br /><b>Reference 3</b>: {expression/expr4} <br /><b>Reference 4</b>: {expression/expr5} <br /><b>Image</b>: <a href="{expression/expr6}" target="_blank">PDF</a></p>

// stamping propper/no-data
IIf (IsEmpty($feature.Stamping), 'No Data', Proper($feature.Stamping, 'firstword'));

// monument
IIf (IsEmpty($feature.Monument), 'No Data', Proper($feature.Monument, 'firstword'));

// ref1
IIf (IsEmpty($feature.Ref1), 
'No Data', Proper($feature.Ref1, 'firstword'));

// ref2
IIf (IsEmpty($feature.Ref2), 
'No Data', Proper($feature.Ref2, 'firstword'));

// ref3
IIf (IsEmpty($feature.Ref3), 
'No Data', Proper($feature.Ref3, 'firstword'));

// ref4
IIf (IsEmpty($feature.Ref4), 
'No Data', Proper($feature.Ref4, 'firstword'));

// image
"http://mtbachelor.co.washington.or.us/images/survey/BM/BM_Photos/bm" + $feature["Benchmark_ID"] + ".pdf"



// GEOCONTROL -----------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------



// SURVEY ---------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------

// surveys popup html
<div style="padding: 5px; background-color: rgb(104, 104, 104);"><font color="#ffffff" face="Verdana" size="3"><b>Survey</b></font></div><p style="margin: 0in;"><font face="Tahoma" size="2"><b>Survey Number: </b>{SurvNum}</font></p><p style="margin: 0in;"><font face="Tahoma" size="2"><b>Image: </b></font><a href="{expression/expr0}" rel="nofollow ugc" target="_blank">PDF</a><font face="Tahoma" size="2"><b> </b></font></p><p style="margin: 0in;"><font face="Tahoma" size="2"><b>Surveyor: </b>{SurveyorName} </font></p><p style="margin: 0in;"><font face="Tahoma" size="2"><b>Client: </b></font>{Client}</p><p style="margin: 0in;"><font face="Tahoma" size="2"><b>Date of Survey: </b>{Date_Survey}</font></p><p style="margin: 0in;"><font face="Tahoma" size="2"><b>Filed Date: </b></font>{expression/expr2}<br /><b>TRS</b>: <br />{expression/expr1}</p>

// survey image
"http://mtbachelor.co.washington.or.us/images/survey/Surveys/" + $feature.SurvNum + ".pdf"


// surveys related trs

// Acess realted table as a FeatureSet
//I used a relate in ArcGIS Pro
var portal = Portal('https://gisint.co.washington.or.us/portal/')
var Survey_TRS = FeatureSetByPortalItem(portal,
    "42021425a5bd49ee947f5e8d33956798", 42, [ 'SurvNum','TRSQTR'])

// Filter related features by using a common attribute
// Here both table have identical SURVNUM feilds
var SURVNUM = $feature.SurvNum
var filterStatement = 'SURVNUM = @SURVNUM'

// Related features as a variable
var relatedData = Filter(Survey_TRS, filterStatement)

// Sort related features by oldest to newest
var relatedDataSorted = OrderBy(relatedData, 'TRSQTR')

// Build the pop-up string by iterating through all related features
var popupString = ''
for (var f in relatedDataSorted){
    
    popupString += Text(f.TRSQTR) + TextFormatting.NewLine
    
        "TRSQTR: " +
        DefaultValue(f.TRSQTR, 'no data') + TextFormatting.NewLine +
        TextFormatting.NewLine
        // USE if you have more than one filed to show in the popup.

}

DefaultValue

(popupString, 'No Data')

// surveys file data 'no data'
IIf (IsEmpty($feature.Filed), 'No Data', $feature.Filed );

// -------------------------------------------------------------------------------------------------------
// COUNTY ROAD by road number ----------------------------------------------------------------------------

// county road popup
<font color="#ffffff" face="Verdana" size="3" style=""><b style="">County Road by road number</b></font></div><p style="margin: 0in;"><b>Road Num</b>: {CRNUM}<br /></p>

IIf // dummy to remove error squigs

// -------------------------------------------------------------
 
 // -------------------------------------------------------------------------------------------------------
// DEDICATIO ----------------------------------------------------------------------------

// dedication popup html
<div style="padding: 5px; background-color: rgb(0, 112, 255);"><font color="#ffffff" face="Verdana" size="3"><b>Dedication</b></font></div><p style="margin: 0in;"><b>Year</b>: {DD_year}<br /><b>Dedication Num</b>: {DD_Num}<br /><a href="{expression/expr0}" target="_blank">Dedication Deed</a><br /></p>



// document hyperlinks
// road vacations
"http://mtbachelor.co.washington.or.us/images/survey/CoRoads/Road_Vacation/vac" + Text($feature["Vac_num"]) + ".pdf"

// plats
// plat names have special characters that can't be in PDF names.
var string = Replace($feature.Platname, ':','-')
var new = Replace(string, '/','')

"https://mtbachelor.co.washington.or.us/images/survey/Plats/" + new + ".pdf"

// surveys
"http://mtbachelor.co.washington.or.us/images/survey/Surveys/" + $feature.SurvNum + ".pdf"

// dedications
"http://mtbachelor.co.washington.or.us/images/survey/DEDICATIONS/" + $feature["DD_Num"] + ".pdf"

// county roads
"http://mtbachelor.co.washington.or.us/images/survey/CountyRoad/CR" + $feature.CRNUM + ".pdf"

// ------------------------------------------------------------------------------------------------------
// ADDRESSES --------------------------------------------------------------------------------------------
// unit number expression
IIf (IsEmpty($feature["UNIT_NUMBER"]), '', ', Unit ' + $feature["UNIT_NUMBER"]);

// address document
"http://mtbachelor.co.washington.or.us/images/survey/AddressMaps/" + Left($feature["TAXLOT"], 3)  + 'W' + Mid($feature["TAXLOT"], 3, 2) + ".pdf"

// -------------------------------------------------------------------------------------------------------
// TAX LOTS ----------------------------------------------------------------------------------------------

// get sub-tax map 
var num = '2N5000006500'

var v0 = MID(num, 3, 1)
var v1 = MID(num, 5, 2)
var v2 = MID(num, 6, 1)
var v3 = MID(num, 5, 1)
var v4 = MID(num, 6, 1)

var l3 = Left(num, 3)
var l5 = Left(num, 5)
var l6 = Left(num, 6)
var l7 = Left(num, 7)

var p1 = "https://pdoclsde1.co.washington.or.us/images/colortaxmaps/"
var p2 = ".pdf"

if (v0 == '0'){
    return p1 + l3 + p2
}
else if (v1 == '00'){
    return p1 + l5 + p2
}
else if (v3 != '0' && v2 == '0'){
    return p1 + l6 + p2
}

else if (v3 != '0' && v2 != '0'){
    return p1 + l7 + p2
}
else {
    
    return p1 + '0000' + p2
}

// get tax map
// evaluates TLID to pass correct string to url 
// to get the correct tax map.
// main tax map 
// 12/20/2022

// evaluates TLID to pass correct string to url 
// to get the correct tax map.
var tlid = $feature.TLID    // '3S1060000301'

var gn = MID(tlid, 0, 7)
var m1 = MID(tlid, 3, 2)
var m2 = MID(tlid, 5, 2)
var m3 = MID(tlid, 3, 4)
var m4 = MID(tlid, 5, 1)
var m5 = MID(tlid, 6, 1)


var l3 = Left(tlid, 3)
var l5 = Left(tlid, 5)
var l6 = Left(tlid, 6)

var p1 = "https://mtbachelor.co.washington.or.us/images/colortaxmaps/"
var p2 = ".pdf"

//tests for 3 char taxmaps
if (m1 == '00'){
    if (m3 == '0000') {
        gn = l3
    }
    if (m3 != '0000') {
        gn = l3 + m4
    }
}
// returns 5 char taxmap if above is false
else if (m2 == '00'){
    gn = l5
    //return p1 + l5 + p2
}
else if (m5 == '0'){
    gn = l6
    
}
return p1 + gn + p2
