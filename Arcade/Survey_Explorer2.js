
// Color Block Popup Header
<div style="padding: 5px; background-color: rgb(170, 102, 205);"><b style="">
<font color="#ffffff" face="Tahoma" size="3" style="">{projName_4}</font></b></div><p style="margin: 0in;"><br /></p>

// image to PDF - taxmap example
"https://pdoclsde1.co.washington.or.us/images/pdfbuilderasp/tiff2pdf.asp?doctype=taxmaps&imageto={expression/expr1}"

// gecontrol link from iSpirits
javascript:sendImage('gc49_1','geocontrol')

// corners -----------------------------------------------------
// -------------------------------------------------------------
// popup html

// returns an attached image
// resulting expression is placed in the pop-up media URL+
// source - https://youtu.be/MzfxBskoon8

var Part1 = "https://gisint.co.washington.or.us/server/rest/services/LUT_ETS/Corner_Fieldnotes/FeatureServer/91/"
var ObjectID = $feature.OBJECTID
var Part2 = "/attachments/"
var AttachID = $feature.AttachID

return Part1 + ObjectID + Part2 + AttachID


// corner - desciption proper case
Proper($feature.DESCRIPTION, 'firstword')

// corner - image
"http://mtbachelor.co.washington.or.us/images/survey/dev/BTBooks/" + $feature["CORNER_ID"]  +  ".pdf"

// corner - site photo
"http://mtbachelor.co.washington.or.us/images/survey/BTBOOKS/SitePhoto/" + $feature["CORNER_ID"] + ".pdf"

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


// Benchmarks ---------------------------------------------------
// --------------------------------------------------------------

// corlor header
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



// geocontrol -------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------




// county road by road number ----------------------------------------------------------------------------
// county road popup
<font color="#ffffff" face="Verdana" size="3" style=""><b style="">County Road by road number</b></font></div><p style="margin: 0in;"><b>Road Num</b>: {CRNUM}<br /></p>

// -------------------------------------------------------------
 




// document hyperlinks
// road vacations
"http://mtbachelor.co.washington.or.us/images/survey/CoRoads/Road_Vacation/vac" + Text($feature["Vac_num"]) + ".pdf"

// plats
"http://mtbachelor.co.washington.or.us/images/survey/dev/Plats/" + $feature.Platname + ".pdf"

// surveys
// "http://mtbachelor.co.washington.or.us/images/survey/dev/Surveys/" + $feature.SurvNum + ".pdf"
var survnum = $feature.SurvNum

//tests for 3 char taxmaps
if (survnum <= 5000){
   return "https://mtbachelor.co.washington.or.us/images/survey/surveys/5000/" + survnum + ".pdf"
}
 if (survnum > 5000 && survnum <= 10000){
    return "https://mtbachelor.co.washington.or.us/images/survey/surveys/10000/" + survnum + ".pdf"
}
   if (survnum > 10000 && survnum <= 15000){
    return "https://mtbachelor.co.washington.or.us/images/survey/surveys/15000/" + survnum + ".pdf"
}
     if (survnum > 15000 && survnum <= 20000){
      return "https://mtbachelor.co.washington.or.us/images/survey/surveys/20000/" + survnum + ".pdf"
}
      if (survnum > 20000 && survnum <= 25000){
       return "https://mtbachelor.co.washington.or.us/images/survey/surveys/25000/" + survnum + ".pdf"
}
       if (survnum > 25000 && survnum <= 30000){
        return "https://mtbachelor.co.washington.or.us/images/survey/surveys/30000/" + survnum + ".pdf"
}
        if (survnum > 30000 && survnum <= 35000){
         return "https://mtbachelor.co.washington.or.us/images/survey/surveys/35000/" + survnum + ".pdf"
}
         if (survnum > 35000 && survnum <= 40000){
          return "https://mtbachelor.co.washington.or.us/images/survey/surveys/40000/" + survnum + ".pdf"
}
          if (survnum > 40000 && survnum <= 45000){
           return "https://mtbachelor.co.washington.or.us/images/survey/surveys/45000/" + survnum + ".pdf"
}


// dedications
"http://mtbachelor.co.washington.or.us/images/survey/DEDICATIONS/" + $feature["DD_Num"] + ".pdf"

// county roads
"http://mtbachelor.co.washington.or.us/images/survey/dev/CountyRoad/CR" + $feature.CRNUM + ".pdf"


// ADDRESSES
// unit number expression
IIf (IsEmpty($feature["UNIT_NUMBER"]), '', ', Unit ' + $feature["UNIT_NUMBER"]);

// address document
"http://mtbachelor.co.washington.or.us/images/survey/AddressMaps/" + Left($feature["TAXLOT"], 3)  + 'W' + Mid($feature["TAXLOT"], 3, 2) + ".pdf"


// DLC
// labels
$feature.LASTNAME + ", " + $feature.FIRSTNAME + TextFormatting.NewLine + "Claim #" + $feature.CLAIM