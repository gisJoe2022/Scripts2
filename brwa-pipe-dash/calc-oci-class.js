// BRWA Pipe Dashboard OCI Class Arcade Expression
// This Arcade expression is used in the BRWA Pipe Dashboard to classify pipe segments based on their estimated OCI (Overall Condition Index). 
// The expression assigns a class from 1 to 5 based on the value of the estimated OCI, with lower values indicating better condition. 
// If the estimated OCI is less than 25, it is classified as 1; if it is between 25 and 50, it is classified as 2; if it is between 50 and 75, 
// it is classified as 3; if it is between 75 and 100, it is classified as 4; and if it is 100 or above, it is classified as 5.
// Joe Hayes: 5/4/2026

var oci = $feature.estimatedOCI;
//var ty = Year(Now());

if (oci <25){
    1
    }
    else if (oci >= 25 && oci < 50){
      2
    }
    else if (oci >= 50 && oci < 75){
      3
    }
    else if (oci >= 75 && oci < 100){
      4
    }
   