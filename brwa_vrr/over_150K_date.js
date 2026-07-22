

var targetMiles = 150000;
var currentMiles = DefaultValue($feature.CurUsage, 0);
var avgDailyUsage = DefaultValue($feature.AvgDaily, 0);

// Can't calculate if average daily usage is zero or negative
if (avgDailyUsage <= 0) {
    return null;
}

// If already over 150,000, return today's date
if (currentMiles > targetMiles) {
    return DateOnly();
}

// Days until the vehicle goes OVER 150,000
var daysUntilOver = Floor((targetMiles - currentMiles) / avgDailyUsage) + 1;

// Return a DateOnly value
return DateAdd(DateOnly(), daysUntilOver, 'days');