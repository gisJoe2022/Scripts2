//tax map expression
var lotid = $feature.TLID
var fivedig = Left(lotid, 5)
var seventest = MID(lotid, 5, 2)
var sevendig = Left(lotid, 7)

if (sevetest == "OO"){
    return "http://mtbachelor.co.washington.or.us/images/survey/dev/TaxMapPDF/" + Left($feature.TLID, 5) + ".pdf"
}
else{
    return "http://mtbachelor.co.washington.or.us/images/survey/dev/TaxMapPDF/" + Left($feature.TLID, 7) + ".pdf"
}

//new one
var seven = "http://mtbachelor.co.washington.or.us/images/survey/dev/TaxMapPDF/" + Left($feature.TLID, 7) + ".pdf"
var five = "http://mtbachelor.co.washington.or.us/images/survey/dev/TaxMapPDF/" + Left($feature.TLID, 5) + ".pdf"
var lotid = $feature.TLID
var seventest = MID(lotid, 5, 2)



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