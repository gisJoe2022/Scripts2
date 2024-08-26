// Grabs data from a related table
// Builds a hyperlink to the image
// Replaces the path to the image
// Returns the hyperlink as a string
// Author: Nels Michaelson
// DATE: 8/11/2024


var portal = Portal('https://gis.clark.wa.gov/portalpw/')
var Stmdocs = FeatureSetByPortalItem(portal,
    "4b35b095430d47d699dea875e62dd0b6", 3, ["*"]) //42 is the table ID in the service

// Filter related features by using a common attribute
// Here both table have identical MMSID fields
var MMSID = $feature.MmsId
var filterStatement = 'MMSID = @MMSID'

// Related features as a variable
var relatedData = Filter(Stmdocs, filterStatement)

// Sort related features by oldest to newest
var relatedDataSorted = OrderBy(relatedData, 'MmsId')
var recordcount = Count(relatedDataSorted)
// Build the pop-up string by iterating through all related features ideally as hyperlinks
var thenewpath = ''
var theurl = ''
var output = []
if (recordcount == 0) {
  Push(output, '0 Images Found')
}

for (var f in relatedDataSorted){
    thenewpath = Replace(f.filepath, 'olympus', '')
    thenewpath = Replace(thenewpath, 'gisdata', '')
    thenewpath = Replace(thenewpath, 'Images', 'ccimages')
    thenewpath = Replace(thenewpath, '\\', '/')
    thenewpath = Replace(thenewpath, '////', 'https://gis.clark.wa.gov/')
    theurl = "<a href=" + TextFormatting.DoubleQuote + thenewpath + TextFormatting.DoubleQuote + ">Image</a>"
    Push(output, theurl)
    }

return { 
  type : 'text', 
  text : `<b>Image Links:</b> ${Concatenate(output, TextFormatting.NewLine)}`
}
