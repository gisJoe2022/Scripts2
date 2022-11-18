
// Replaces text values ina field with new values. Example:
// 1. Original text = '51 east entrance', replacement text = 'East Entrance'
// 2. Original text = '54 middle entrance', replacement text = 'Middle Entrance'
// 3. Original text = '1', replacement text = 'West Entrance'

// Deosn't work in AGOL pop-ups
var Gate_Number = $feature.Gate_Number; 
    if (Gate_Number == '51 east entrance') {Gate_Number = 'East Entrance';} 
        else if (Gate_Number == '54 middle entrance') {Gate_Number = 'Middle Entrance';} 
            else if (Gate_Number == '1') {Gate_Number = 'West Entrance';} 
            
return Gate_Number;
