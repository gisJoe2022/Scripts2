#-------------------------------------------------------------------------------
# Name:        DownloadStr
# Purpose:     Downloads the weekly maintained streets file from Metro's server
#
# Author:      RebekahB
# Updated by   RReise
#
# Created:     02/07/2015
# Updated:     10/17/2022
# Copyright:   (c) RebekahB 2015
#-------------------------------------------------------------------------------

import os, sys
cmd_folder = "\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from DataTransfer.modFTP_3_7 import FTP_Download
import gbl, trktime
from modEmail_3_7 import Send
import zipfile

Title = 'Str.zip dowload'
Message=''
Error = 0

# # Change to MyEmailRyan for dev
# EmailTo = gbl.MyEmailRyan
# !!!!Change back to GroupEmail when moving to Prod!!!.
EmailTo = gbl.GroupEmail

host='ftp.oregonmetro.gov'
user='washco'
password='sobupavi'
dirn=''
filename='str.zip'
saveloc= gbl.StrSave

try:
    print ("Import str.zip from Metro Server")
    Temp = FTP_Download(host,user,password,dirn,filename,saveloc)
    Message = Message + Temp.appendMessage
    Error = Error + Temp.fail

    if Error >0:

        Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
        Send(Title, Message, Error, EmailTo)
    else:
        try:
            zip = zipfile.ZipFile(gbl.StrSave+filename)
            zip.extractall(gbl.StrSave)
            Message= Message + "\n" + "Zip Extract Succeeded"
            print (Message)
        except:
            Error=Error+1
            Message= Message + "\n" + "Zip Extract Failed"
        Send(Title, Message, Error, EmailTo)

except:
    print ("FTP failed")
    Message = Message + "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
    Send(Title, Message, Error, EmailTo)