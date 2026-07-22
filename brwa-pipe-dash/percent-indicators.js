


var m = Round($datapoint.SUM_SHAPE__LENGTH/5280, 1)
var r = Round($reference.SUM_SHAPE__LENGTH/5280, 1)

var difference = m-r;
var absoluteDifference = abs(difference);
var ratio = m/r;
var ratioChange = difference/r;
var percentage = Round(ratio*100, 0);
var percentChange = ratioChange*100

return {
  //textColor:'',
  //backgroundColor:'',
  topText: percentage+"%",
  topTextColor: '#ab05a8ff',
  topTextOutlineColor: '',
  topTextMaxSize: 'medium',
  middleText: m+' mi',
  middleTextColor: '',
  middleTextOutlineColor: '',
  middleTextMaxSize: 'small',
  bottomText:r+" mi",
  bottomTextColor: '',
  bottomTextOutlineColor: '',
  bottomTextMaxSize: 'medium',
  //iconName:'',
  //iconAlign:'left',
  //iconColor:'',
  //iconOutlineColor:'',
  //noValue:false,
  //attributes: {
    // attribute1: '',
    // attribute2: ''
  // }
}