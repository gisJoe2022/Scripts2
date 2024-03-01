


// this one works
var getData = FeatureSetByName($datastore, "Plat", ["Filename", "Recorded"])
var platint = Intersects(getData, $feature)

var platlist = []
//var newarray = []

for (var k in platint){
    var rdate = k.Recorded
    var newdate = Right(rdate, 4)
    var numdate = Number(newdate, '####')
        Push(platlist, numdate)
}

return Max(platlist)
//return plat_list
//if (Val == null) return "https://mtbachelor.co.washington.or.us/images/survey/NoImage.pdf" 
//"https://mtbachelor.co.washington.or.us/images/survey/Plats/" + Text(Val.Filename)


//-----------------------------------------------------------------------------------



// snipet
var getData = FeatureSetByName($datastore, "Plat", ["Filename", "Recorded"])
var PlatDataInt = Intersects(getData, $feature)

var platlist = ""
//var newarray = []

for (var k in PlatDataInt){
    platlist += Right(k.Recorded, 4) + TextFormatting.NewLine
}

return platlist
//return plat_list
//if (Val == null) return "https://mtbachelor.co.washington.or.us/images/survey/NoImage.pdf" 
//"https://mtbachelor.co.washington.or.us/images/survey/Plats/" + Text(Val.Filename)


//------------------------------------------------------------------------------


// does not work
var platlist = ""
var newarray = []

for (var k in PlatDataInt){
    platlist += Right(k.Recorded, 4) + "," //TextFormatting.NewLine
     if (Number(platlist[k]) < 300000){
       Push(newarray, platlist[k]);
   } 
}
return Max(newarray)
//return plat_list
//if (Val == null) return "https://mtbachelor.co.washington.or.us/images/survey/NoImage.pdf" 
//"https://mtbachelor.co.washington.or.us/images/survey/Plats/" + Text(Val.Filename)


//------------------------------------------------------



// snipet
//store SiteID as a variable so it can be used to query
//the BacteriaSamples table for matching records

var siteId = $feature.SITEID

//access BacteriaSamples table as a FeatureSet;
//include only three relevant fields and filter on QA/QC status
var samplesAll = Filter(FeatureSetById($map, /* Watershed - BacteriaSamples */ "Watershed_962", ['SAMPLEDATE', 'SITEID','MPN_ECOLI']), "QAQC_COMPL = 'yes'")

//use SQL filter statement to access variable with @ symbol;
//essentially this creates a relate
var filterStatement = "SITEID = @siteId"

//filter the table to find related records at each site
var samplesBysite = Filter(samplesAll, filterStatement)

//store count of related records as a variable
var cnt = Count(samplesBysite)
Console("Number of Samples: " + cnt)

//loop through samples to find the highest MPN_ECOLI
//rating criteria: <= 100 'Good'; 101-405 'Fair'; >405 'Poor'
//set starting value of variable to highest possible 'Good' rating
var highest_mpn = 100
var rating = ''
if (cnt > 0) {
    for(var f in samplesBysite){
    //if sample is higher than current highest_mpn value, update it
    highest_mpn = When(f.MPN_ECOLI > highest_MPN, f.MPN_ECOLI, highest_MPN) 
        
    }
}else {
    rating = "No samples"
}

//designate site rating based on highest_mpn value
rating = When(highest_mpn <= 100, 'Good', highest_mpn > 405, 'Poor', 'Fair') 

Console("Highest MPN: " + highest_mpn)
Console("Site Rating: " + rating)

return rating

//-----------------------------------------------------------------------------------------------------------

//snipet
//bring in plats recorded field
var getdata = FeatureSetByName($datastore, "Plat", ["Recorded"]);

var platint = Intersects(getdata, $feature);
var platdate = platint.Recorded // intersect address point with plats
var newdate = Right(platdate, 4)
var numdate = Number(newdate)
Console(numdate)
var cnt = Count(platint);// get the count of intersecting plat from platint
//Console(cnt);
var yr = 0 //Year(Now());// gets current year
var ryear = getdata.Recorded // year only from date
//Console(cyear);
var platlist = ""
//var newarray = []
if (cnt > 0){
    for (var k in platint){
        yr = When(k.numdate > yr, yr, yr)
       // maxy = When(k.Recorded > cyear, k.Recorded, cyear)
    }
}else {
    platlist = "No samples"
}
return 

