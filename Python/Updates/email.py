# Script 1: Main script
# Note that you don't require the geoprocessor object in this script.
import win32com.client, sys, os, string, arcgisscripting, arcpy
from win32com.client import Dispatch

# Load required toolboxes...

#Set the Input Values
inDBaseServer = "psqlgis1"
inDBase = "production"
inDBUser = "sde"
inDBUserPwd = "5QYCRCDRJ"
# Create the ADO Connection object via COM.
Conn = win32com.client.Dispatch(r'ADODB.Connection')
# Now set the connection properties via the ConnectionString
Conn.ConnectionString = "Provider=MSDASQL; Driver={SQL Server}; Server=" + inDBaseServer + "; Database=" + inDBase + "; UID=" + inDBUser + "; PWD=" + inDBUserPwd + ";"
print ("Connection String = " + Conn.ConnectionString)
arcpy.AddMessage ("Connection String = " + Conn.ConnectionString)
Conn.Open()
# Build and Execute SQL Statement to database
sqlSelectStatement = "SELECT *  FROM dbo.v_layers_to_copy where disabled = 0 and schedule = 'DAILY'"
print(sqlSelectStatement)
(oRS, result)  = Conn.Execute(sqlSelectStatement)
import datetime
import smtplib
import base64

now = datetime.datetime.now()
filename = "D:\\GIS_data_updates\\DailyWeekly\\" + (now).strftime('%Y-%m-%d') +"msggis.txt" 
f = open(filename, "w")
f.write('Subject: Email - Nightly Layer copy \r\n') 
f.write('Email - Report for Nightly PSQLGIS1 Layer Append Process - ' + str(now) + '\n' )
f.write ('\n')  # Added for logfile clarity, By: RichardC Date: 20151012
f.close()

while not oRS.EOF:	
	fromlayer =  oRS.Fields.Item("fromlayer").Value
	tolayer =   oRS.Fields.Item("tolayer").Value
	print fromlayer
	print tolayer
	pythonPath = 'D:\\Python27\\ArcGIS10.6\\python.exe'

  	layercopyScript = 'D:\\GIS_data_updates\\DailyWeekly\\calledprocess_append_features_tolayer.py'
  	layerdeleteScript = 'D:\\GIS_data_updates\\DailyWeekly\\calledprocess_delete_features_fromlayer.py'
	layerupdateresultstatusScript= 'D:\\GIS_data_updates\\UtilityScripts\\calledprocesswriteappendoperationtoDB.py'	
 
 	inputlayername = oRS.Fields.Item("fromdataconnection").Value
	outputlayername = oRS.Fields.Item("todataconnection").Value
	layerid = str(oRS.Fields.Item("theid").Value)

	parameterList = []
	parameterList.append('python.exe')
	# second parameter is the full path of the Python script
	parameterList.append(layercopyScript)
	parameterList.append(inputlayername)
	parameterList.append(outputlayername)
        parameterList.append(layerid)


	parameterList2 = []
	parameterList2.append('python.exe')
	# second parameter is the full path of the Python script
	parameterList2.append(layerdeleteScript)
	parameterList2.append(outputlayername)

         
	parameterList3 = []
	parameterList3.append('python.exe')
	parameterList3.append(layerupdateresultstatusScript)
	# the following parameters are the arguments for the Clip script
        parameterList3.append(layerid)
	parameterList3.append('0')


	inputlayername = inputlayername.replace('%',' ')
	ouputlayername = outputlayername.replace('%',' ')
	print inputlayername
        print ouputlayername
	if arcpy.Exists(inputlayername):
		if arcpy.Exists(ouputlayername):
			print "Running delete layer"
			os.spawnv(os.P_WAIT, pythonPath, parameterList2)
			print "Running append layer"
			os.spawnv(os.P_WAIT, pythonPath, parameterList)
		else:
			print "aborting process output layer does not exist"
			os.spawnv(os.P_WAIT, pythonPath, parameterList3)
			logfile = open(filename, "a")  
			themessage = 'Error occured on - ' + ouputlayername + ' - output layer does not exist' + '\n'
			logfile.write(themessage)
			logfile.write('Time - ' + str(datetime.datetime.now()) + '\n' )
			logfile.write('Status - ' + arcpy.GetMessages() + '\n' )
			logfile.write('\n')     # Added for logfile clarity, By: RichardC Date: 20151005
			logfile.close()
	else:
		print "aborting process input layer does not exist"
		os.spawnv(os.P_WAIT, pythonPath, parameterList3)
		logfile = open(filename, "a")  
		themessage = 'Error occured on - ' + inputlayername + ' - input layer does not exist' + '\n'
		logfile.write(themessage)
		logfile.write('Time - ' + str(datetime.datetime.now()) + '\n' )
		logfile.write('Status - ' + arcpy.GetMessages() + '\n' )
		logfile.write('\n')     # Added for logfile clarity, By: RichardC Date: 20151005
		logfile.close()
	oRS.MoveNext()

#send email report
smtpserver = 'smtp.co.washington.or.us'
AUTHREQUIRED = 0 # if you need to use SMTP AUTH set to 1
smtpuser = '' # for SMTP AUTH, set SMTP username here
smtppass = '' # for SMTP AUTH, set SMTP password here

# Read a file and encode it into base64 format
fo = open(filename, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)  # base64

## sender = 'itsdbagisnotify@co.washington.or.us'
## receiver = ['itsdbagisnotify@co.washington.or.us']
sender = 'brian_hanes@co.washington.or.us'
receiver = ['brian_hanes@co.washington.or.us','richard_crucchiola@co.washington.or.us'] 

marker = "AUNIQUEMARKER"

body ="""
See attached report for process results
"""
# Define the main headers.
part1 = """From: GIS Notification <itsdbagisnotify@co.washington.or.us>
To: GIS Report notification forupdate <Brian_Hanes@co.washington.or.us>
Subject: Sending Attachement - Results for Nightly SDE Append Process
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

# Define the message action
part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

# Define the attachment section
part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)
message = part1 + part2 + part3

try:
   smtpObj = smtplib.SMTP(smtpserver)
   smtpObj.sendmail(sender, receiver, message)
   print "Successfully sent email"
except Exception:
   print "Error: unable to send email"


oRS.Close()
Conn.Close() 