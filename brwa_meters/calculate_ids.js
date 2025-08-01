// This Arcade expression generates a unique identifier for each meter
// The identifier is composed of a fixed text prefix and a sequential number formatted with leading zeros.  
// The sequential number is derived from the SeqNum field of the feature.
// The final output is a string that combines the prefix and the formatted sequential number.
// The seqNum field values are acalculated using the Python squencial number function.
// Author: Joe Hayes
// Date: 2025-06-28

var text1 = 'MET'
var num1 = Text($feature.SeqNum, '0000000')

text1 + num1