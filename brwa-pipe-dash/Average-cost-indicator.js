


var sum = $datapoint.SUM_ACTIVITYCOST;
var pyr = Text(Round(sum/75), '#,###');

return {
  //textColor:'',
  //backgroundColor:'',
  topText: 'Average Cost',
  topTextColor: '',
  topTextOutlineColor: '',
  topTextMaxSize: 'medium',
  middleText: '$'+pyr,
  middleTextColor: '#3aab05',
  middleTextOutlineColor: '',
  middleTextMaxSize: 'large',
  bottomText: 'per Year (Thousands)',
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

