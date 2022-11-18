// Acess 'Groundwater Levels Monthly Mean' table as a FeatureSet
var portal = Portal("https://www.arcgis.com")
var waterLevels = FeatureSetByPortalItem(portal,
    "426460a6ae7c47b5acb9a64294bd3dcb", 0, ['STATION', 'MSMT_DATE',
    'RPE_WSE', 'GSE_WSE', 'WSE'])

// Filter related features by using a common attribute
var STATION = $feature.STATION
var filterStatement = 'STATION = @STATION'

// Related features as a variable
var relatedData = Filter(waterLevels, filterStatement)

// Sort related features by oldest to newest
var relatedDataSorted = OrderBy(relatedData, 'MSMT_DATE ASC')

// Build the pop-up string by iterating through all related features
var popupString = ''
for (var f in relatedDataSorted){
    
    popupString += Text(f.MSMT_DATE, 'MMMM Y') + TextFormatting.NewLine +
    
        "Depth to water surface (ft): " +
        DefaultValue(f.RPE_WSE, 'no data') + TextFormatting.NewLine +
        
        "Depth below ground surface (ft): " +
        DefaultValue(f.GSE_WSE, 'no data') + TextFormatting.NewLine +
        
        "Water Surface Elevation (ft): " +
        DefaultValue(f.WSE, 'no data') + TextFormatting.NewLine +
        TextFormatting.NewLine
}

DefaultValue(popupString, 'No measurements to show')