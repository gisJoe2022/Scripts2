/* In the above example, replace 'related_table_name' with the name of the related 
table you want to retrieve features from. Replace 'attribute_name' with the name 
of the attribute you want to use as the link text. And replace 
'https://myserver.com/mapviewer/' with the base URL of your web application.

This script will iterate over all related features and construct a hyperlink that 
includes the OBJECTID of the related feature in the URL. You can customize the URL 
to include any other information you need.
 */
var relatedFeatures = FeatureSetById($feature, 'related_table_name');
var hyperlink = "";

for (var i in relatedFeatures) {
  var feature = relatedFeatures[i];
  var url = 'https://myserver.com/mapviewer/?feature=' + feature.OBJECTID;
  hyperlink += '<a href="' + url + '">' + feature.attribute_name + '</a><br/>';
}

return hyperlink;
