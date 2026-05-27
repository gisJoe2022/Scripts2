


// --- Reference the three layers ---
var layer1 = FeatureSetByName($map, "Gravity Main Sewer", ["ActivityCost"], false);
var layer2 = FeatureSetByName($map, "Force Main Sewer", ["ActivityCost"], false);
//var layer3 = FeatureSetByName($map, "Layer 3 Name", ["ActivityCost"], false);

// --- Combine all features into one logical set ---
var allFeatures = Union(layer1, layer2);

// --- Calculate total cost and count ---
var totalCost = 0;
var countFeatures = 0;

for (var f in allFeatures) {
    if (!IsEmpty(f.ActivityCost)) {
        totalCost += f.ActivityCost;
        countFeatures += 1;
    }
}

// --- Prevent divide-by-zero ---
if (countFeatures == 0) {
    return {
        type: "number",
        value: 0
    };
}

// --- Average activity cost ---
var averageCost = totalCost / countFeatures;

// --- Divide by 75 years ---
var result = averageCost / 75;

// --- Return value for Indicator ---
return {
    type: "number",
    value: result
};