// arcade symbology code.
// this one used in the Corners app to color code the 
// the point class symbols by year.

// joe hayes January 2023

// loop through unique values t make symbol class
var uniqueValues = Distinct($feature.RepYear3); // Get unique values from the field
var func = funtion(value);
ForEach(uniqueValues, func); {
    if ($feature.RepYear3 == func); {
        // Create a symbol based on the 'value' (e.g., color, size, etc.)
        return  new SimpleMarkerSymbol({ 
            color:  If(value == "Category1", Color.Red, If(value == "Category2", Color.Blue, Color.Green)), 
            size: 10
        });
    }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////

