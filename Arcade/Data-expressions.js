
// This sample calculates the total amount of water lost for each leak in a dataset 
// of water leaks in the city of San Francisco. The total amount of water lost is 
// calculated by multiplying the leak rate (in gallons per day) by the number of days 
// the leak has been active. The resulting value is returned as a new field called "leak_amount".
var portal = Portal('https://www.arcgis.com');
var fs = FeatureSetByPortalItem(
    portal,
    '9ad3138c16dd4c20aca6ca2a1b14dc89',
    9,
    [
        'LEAKRATE',
        'LeakDays'
    ],
    false
);

return GroupBy(
    fs,
    'objectid',
    {
        name: 'leak_amount',
        expression: 'LEAKRATE * LeakDays',
        statistic: 'SUM'
    }
)