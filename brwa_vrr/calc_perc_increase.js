// Calculate the percentage increase in replacement cost over time AND formats the replacement year as text.
// current replacement cost, the number of years since it was last replaced, 
// and a fixed annual increase rate. The formula used is:
// Future Replacement Cost = Current Replacement Cost * (1 + Annual Increase Rate) ^ Number of Years
// The result is rounded to the nearest whole number.
// author: Joe Hayes
// date: 2026-03-04

// --- Inputs from the current row ---
// --- Inputs from the current row ---
// --- Inputs from the current row ---
var cost = $datapoint.Repl_Cost_Current;
var formatcost = Text($datapoint.Repl_Cost_Current, '$###,###')
var repYear = $datapoint.Rep_Year;

// --- Null/empty safeguards ---
if (IsEmpty(cost) || IsEmpty(repYear)) {
  return {
    textColor: '#000000',
    backgroundColor: '#ffffff',
    separatorColor: '#e5e7eb',
    selectionColor: '',
    selectionTextColor: '',
    attributes: {
      replaceCost: null,
      note: 'Missing inputs'
    }
  };
}

// --- Time and rate settings ---
var years = repYear - Year(Now())
// Rate as a percent: 3% → 0.03
var rate = 3/100;
// --- Compound growth: cost * (1 + rate)^years ---
var replaceCost = cost * Pow(1 + rate, years);
var formatrepcost = Text(replaceCost, '$###,###')
// Optional: round to whole dollars
var replaceCostRounded = Round(replaceCost, 0,);
var nyear = Text($datapoint.Rep_Year);
// --- Return the formatting dictionary ---
return {
  textColor: '#ffffff',
  backgroundColor: '#28282B',
  separatorColor: '#e5e7eb',   
  selectionColor: '',
  selectionTextColor: '',
  attributes: {
    ReplaceCost: replaceCostRounded,   // <-- use {expression/ReplaceCost} in your template
    newYear: nyear,
    formatrepcost:formatrepcost,
    formcurcost: formatcost
  }
};
