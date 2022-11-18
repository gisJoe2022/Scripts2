
//

// Submitted - {expression/expr0}
if ($feature.status == 'Submitted') {
    return 'background-color:#C93100'
}
return 'background-color:#DDDDDD'

//received - {expression/expr1}
if ($feature.status == 'Received') {
    return 'background-color:#E89D00'
}
return 'background-color:#DDDDDD'

//In Progress - {expression/expr2}
if ($feature.status == 'In Progress') {
    return 'background-color:#FFD700'
}
return 'background-color:#DDDDDD'

//Resolved - {expression/expr3}
if ($feature.status == 'Completed') {
    return 'background-color:#83C96E'
}
return 'background-color:#DDDDDD'

//Is Resolved - {expression/expr4}
IIF($feature.status == "Completed", null, "none");

//Resolution Time - {expression/expr5}
var days = Round(DateDiff($feature.resolutiondt, $feature.CreationDate,"days"), 0)
var day_text = Text(days);
return IIF(day_text == "NaN", null, days + " days");

//Full Name - {expression/expr6}
if ($feature.pocfullname != null) {
    return $feature.pocfullname;
}
var name = null;

if ($feature.pocfirstname != null) {
name = $feature.pocfirstname;
}

if ($feature.poclastname != null) {
if (name != null) {
   name = name + " " + $feature.poclastname;
}
else {
    name = $feature.poclastname;
}
}  

return name;

//Popup html
<div style="padding: 0px 4px">
<font size="5" style="color:#1973ad;">{probtype}</font><br />
{category} problem reported on {CreationDate}.<br /><br />
<b>Details:</b> {details}
<p></p>
<p style="margin: 0;">{expression/expr6}</p>
<p style="margin: 0;">{pocphone}
</p><p style="margin: 0;"><a href="mailto: {EMAIL}" rel="nofollow ugc">{pocemail}</a></p>
<p></p><p></p>
<b>Location:</b> {locdesc}<br /><br />
<b>Status:</b><br />
<table style="border-collapse: separate; border-spacing: 2px 4px; width: 100%; table-layout: fixed; margin: 0px -2px; max-width: 500px;">
  <tbody><tr height="16">
    <td style="{expression/expr0}; text-align: center; width: 25%"></td>
    <td style="{expression/expr1}; text-align: center; width: 25%"></td>
    <td style="{expression/expr2}; text-align: center; width: 25%"></td>
    <td style="{expression/expr3}; text-align: center; width: 25%"></td>
  </tr>
  <tr height="24" style="text-align: center;">
	<td style="text-align: center; width: 25%; font-weight: normal; padding-left: 0px; word-wrap: break-word;">Submitted</td>
	<td style="text-align: center; width: 25%; font-weight: normal; padding-left: 0px; word-wrap: break-word;">Received</td>
	<td style="text-align: center; width: 25%; font-weight: normal; padding-left: 0px; word-wrap: break-word;">In Progress</td>
	<td style="text-align: center; width: 25%; font-weight: normal; padding-left: 0px; word-wrap: break-word;">Completed</td>
  </tr>
</tbody></table><br />
<b>Assigned To:</b> {assignedto}
<table style=" border-collapse: separate; border-spacing: 0px 0px; width: 100%; table-layout: fixed; margin: 0px -1px;">
	<tbody>
	  <tr>
		<td style="display:{expression/expr4}; text-align: left; width: 100%">		
			<b><br />Resolved On:</b> {resolutiondt}<br /><br />
			<b>Resolution Time:</b> {expression/expr5}<br /><br />
			<b>Resolution:</b> {resolution}<br /><br />
			<a href="mailto:{pocemail}?subject={category}%20Problem%20Report%20Survey&amp;body=Hello%20{expression/expr6}%2C%0D%0A%0D%0AYou%20are%20receiving%20this%20e-mail%20because%20we%20recently%20resolved%20your%20{category}%20-%20{probtype}%20problem%20report.%20Your%20feedback%20is%20important%20to%20us.%20Please%20take%20a%20moment%20to%20complete%20the%20survey%20below%20about%20your%20experience.%0D%0A%0D%0Ahttps%3A%2F%2Fsurvey123.arcgis.com%2Fshare%2F21f80a216abf4386954815d80371ce99?portalUrl=https://washco.maps.arcgis.com%26field:probguid={GLOBALID}%0D%0A%0D%0AThank%20you%20in%20advance%20for%20your%20participation.%20We%20appreciate%20the%20time%20you%20have%20taken%20and%20will%20actively%20use%20it%20to%20improve%20our%20services%20to%20you." rel="nofollow ugc" style="background-color: #1973ad;color: #FFFFFF;padding: 10px 10px;text-decoration: none;margin: 0px auto;width: 220px;display: block;text-align:center;">Send Satisfaction Survey</a>
		</td>
	  </tr>
	</tbody>
</table>
</div>