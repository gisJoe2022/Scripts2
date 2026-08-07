

var yearOld = DefaultValue($feature.vehicle_age, 0);

var fuelType = Upper(DefaultValue($feature.fuel_type, ""));
var purchasePrice = DefaultValue($feature.purchace_price, 0);

var currentMileage = DefaultValue($feature.CurUsage, 0);
var avgDailyUsage = DefaultValue($feature.AvgDaily, 0);

var totalRepairCost = DefaultValue($feature.repair_maintenance, 0);
var annualRepairCost = totalRepairCost/yearOld;

var currentYear = Year(Today());

// ====================================
// AGE PROJECTION
// ====================================

var ageYear = currentYear + Max(0, (15 - yearOld));

// ====================================
// MILEAGE PROJECTION
// ====================================

var mileageTarget = IIF(fuelType == "Diesel", 200000, 150000);
var mileageYear = 9999;

if (currentMileage >= mileageTarget) {
    mileageYear = currentYear;
}
else if (avgDailyUsage > 0) {
    var daysRemaining = (mileageTarget - currentMileage) / avgDailyUsage;
    mileageYear = Year(DateAdd(Today(), daysRemaining, "days"));
}

// ====================================
// REPAIR PROJECTION
// ====================================

var repairThreshold = purchasePrice * 0.50;
var repairYear = 9999;

if (totalRepairCost >= repairThreshold) {
    repairYear = currentYear;
}
else if (annualRepairCost > 0) {
    var yearsRemaining = (repairThreshold - totalRepairCost) / annualRepairCost;
    repairYear = currentYear + Ceil(yearsRemaining);
}

// ====================================
// EARLIEST YEAR
// ====================================

return Min([ageYear, mileageYear, repairYear]);