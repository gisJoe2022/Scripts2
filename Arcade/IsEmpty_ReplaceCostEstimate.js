IIf(IsEmpty($feature["costEst_4"]), Text('No Data'), Text($feature["costEst_4"], '$###,###,###,###'));

IIf (IsEmpty($feature["stName_1"]), 'No Data', $feature["stName_1"]);