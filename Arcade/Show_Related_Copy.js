
// Acess realted table as a FeatureSet
// Don't forget to change the portal url
// don't forget to add the related table as an item to the portal
var portal = Portal('https://gisint.co.washington.or.us/portal/')
var Survey_TRS = FeatureSetByPortalItem(portal,
    "42021425a5bd49ee947f5e8d33956798", 42, [ 'SurvNum','TRSQTR'])

// Filter related features by using a common attribute
// Here both table have identical SurvNum feilds
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

DefaultValue(popupString, 'No Data')