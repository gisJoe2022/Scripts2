
// 1. Access the related records from the destination table
// Replace "Relationship_Name" with your actual relationship class name
var related = FeatureSetByRelationshipName($feature, "sgp_install_verification_table")

return IIf(Count(related) > 0, "Inspected", "Not Inspected");


///////////---------------------------------------------------------------------------------


// 1. Access the related records from the destination table
// Replace "Relationship_Name" with your actual relationship class name
var relatedRecords = FeatureSetByRelationshipName($feature, "sgp_install_verification_table")

// 2. Sort the related table by a date field to find the newest entry
var sortedRecords = OrderBy(relatedRecords, "inspect_date DESC");

// 3. Get the first (most recent) record from that sorted list
var newestRecord = First(sortedRecords);

// 4. Return the value from the destination table field
// Replace "StatusField" with your actual destination table field name
if (newestRecord != null) {
    return newestRecord.Status;
} else {
    return null; 
}