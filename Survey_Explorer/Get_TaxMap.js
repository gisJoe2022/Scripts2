//tax map expression
// main tax map 
// 12/20/2022

// evaluates TLID to pass correct string to url 
// to get the correct tax map.
var tlid = $feature.TLNO    // '3S1060000301'

var gn = MID(tlid, 0, 7)
var m1 = MID(tlid, 3, 2)
var m2 = MID(tlid, 5, 2)
var m3 = MID(tlid, 3, 4)
var m4 = MID(tlid, 5, 1)
var m5 = MID(tlid, 6, 1)

var l3 = Left(tlid, 3)
var l5 = Left(tlid, 5)
var l6 = Left(tlid, 6)

var p1 = "https://mtbachelor.co.washington.or.us/images/colortaxmaps/"
var p2 = ".pdf"

//tests for 3 char taxmaps
if (m1 == '00'){
    if (m3 == '0000') {
        gn = l3
    }
    if (m3 != '0000') {
        gn = l3 + m4
    }
}
// returns 5 char taxmap if above is false
else if (m2 == '00'){
    gn = l5
    //return p1 + l5 + p2
}
else if (m5 == '0'){
    gn = l6
    
}
return p1 + gn + p2

/*
<!---
AUTHOR: Tyler Gundberg, GIS Specialist
DATE: 06.15.2007
PURPOSE: Retures a query of all match Taxmaps for TLNO.

COMPONET: FindImagesTaxmaps.cfc 
FUNCTIONS: 
			GetImages  --  Gets all Images the reference the Taxlot ID Number (TLNO)
--->
<cfcomponent  output="no">

<cffunction name="GetImages" access="public" returntype="query">
		<cfargument name="TLNO" type="string" required="yes">
		<cfargument name="WhereCriteria" type="numeric" required="yes" default="1">
		
<!---  TSG, 05.29.2007; Notes: Updated Scanned Taxmap Search  --->
<!--- -~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ --->
		<cfset SECTNUM1 = MID(ARGUMENTS.TLNO, 4, 2)>
		<cfset SECTNUM2 = MID(ARGUMENTS.TLNO, 6, 2)>
		<cfset SECTNUM3 = MID(ARGUMENTS.TLNO, 4, 4)>
		<cfset SECTNUM4 = MID(ARGUMENTS.TLNO, 6, 1)>
		<cfset SECTNUM5 = MID(ARGUMENTS.TLNO, 7, 1)> 
		
      
		<cfif SECTNUM1 EQ "00">    
		 
			<cfif SECTNUM3 EQ "0000">
				<cfset getImage = Left(ARGUMENTS.TLNO, 3)>
			</cfif>
		
			<cfif SECTNUM4 NEQ "0">
				<cfset getImage = Left(ARGUMENTS.TLNO, 3) & SECTNUM4>
		   </cfif>
			
		<cfelseif SECTNUM2 EQ "00"> 
			<cfset getImage = Left(ARGUMENTS.TLNO, 5)>  
			
		<cfelseif SECTNUM5 EQ "0">
			<cfset getImage = Left(ARGUMENTS.TLNO, 6)>
			
		<cfelse>
			<cfset getImage = Left(ARGUMENTS.TLNO, 7)>
					 
		</cfif>
	
<!--- -~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ --->
			<cfstoredproc procedure="usp_GetTaxmaps" datasource="GISweb">
				<cfprocparam type="In" cfsqltype="CF_SQL_CHAR" variable="groupname" value="#getImage#">
				<cfprocparam type="In" cfsqltype="cf_sql_numeric" variable="wherecriteria" value="#WhereCriteria#">
				<cfprocresult name="qIMAGES">
			</cfstoredproc>
	
	<cfreturn qIMAGES>
</cffunction>
</cfcomponent>
*/
