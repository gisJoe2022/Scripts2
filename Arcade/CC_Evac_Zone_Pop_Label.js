IIf($feature.Level == '3', 'GO NOW', IIf($feature.Level == '2', 'GET SET', IIf($feature.Level == '1', 'GET READY', $feature.Level))
IIf($feature.Level == '3', 'GO NOW', IIf($feature.Level == '2', 'GET SET', IIf($feature.Level == '1', 'GET READY', $feature.Level))


var code = $feature.codedValue;
var decodedValue = Decode(code, 1, 'Residential', 2, 'Commercial', 3, 'Mixed', 'Other');

var code = $feature.Level_;
var decodedValue = Decode(code, 1, 'GET READY', 2, 'GET SET', 3, 'GO NOW!', 'Other');
decodeValue

var checkvalue = $feature.Level_
var ready = 'GET READY!'
var set = 'GET SET!'
var go = 'GO NOW!'
var none = ''
iif(checkvalue=='1',ready, none)