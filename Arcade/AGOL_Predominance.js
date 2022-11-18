// The fields from which to calculate predominance
// The expression will return the alias of the predominant field

var fields = [
  { value: $feature["ARABIC_LTVW_P"], alias: "Arabic" },
  { value: $feature["CHINESE_LTVW_P"], alias: "Chinese" }, 
  { value: $feature["FREMCH_LTVW_P"], alias: "French" },
  { value: $feature["GERMANIC_LTVW_P"], alias: "German" },
  { value: $feature["INDO_EURO_LTVW_P"], alias: "Indo-European" },
  { value: $feature["KOREAN_LTVW_P"], alias: "Korean" },
  { value: $feature["OTHER_API_LTVW_P"], alias: "Other API" },
  { value: $feature["OTHER_UNSPECIFIED_LTVW_P"], alias: "Other Unspecified" },
  { value: $feature["SLAVIC_LTVW_P"], alias: "Slavic" },
  { value: $feature["SPANISH_LTVW_P"], alias: "Spanish" },
  { value: $feature["TAGALOG_LTVW_P"], alias: "Tagalog" },
  { value: $feature["VIETNAMESE_LTVW_P"], alias: "Vietnamese" },
  
];

// Returns the predominant category as the alias
// defined in the fields array. If there is a tie,
// then both names are concatenated and used to
// indicate the tie

function getPredominantCategory(fieldsArray){
  var maxValue = -Infinity;
  var maxCategory = "";
  for(var k in fieldsArray){
    if(fieldsArray[k].value > maxValue){
      maxValue = fieldsArray[k].value;
      maxCategory = fieldsArray[k].alias;
    } else if (fieldsArray[k].value == maxValue){
      maxCategory = maxCategory + "/" + fieldsArray[k].alias;
    }
  }
  return IIF(maxValue <= 0, null, maxCategory);
}

getPredominantCategory(fields);
