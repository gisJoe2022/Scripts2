#-------------------------------------------------------------------------------
# Name:        modFTP.py
# Purpose:      Transfers data from FTP to computer
#
# Author:      RebekahB
#
# Created:     02/07/2015
# Copyright:   (c) RebekahB 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os, sys
cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from ftplib import FTP
import socket
import gbl


msg = gbl.PassMessage()


def FTP_Download(HOST, USER, PASSWORD,DIRN,FILE,SAVELOC):
    try:
        ftp = FTP(HOST)
        print ('ftp connect attempt')
    except (socket.error, socket.gaierror) as e:
        msg.appendMessage = 'ERROR: cannot reach "%s"' % HOST
        msg.fail = 1
        print (msg.appendMessage)
        return msg

    print ('*** Connected to host "%s"' % HOST)


    try:
        ftp.login(USER, PASSWORD)
        print ("ftp login attempt")
    except error_perm:
        msg.appendMessage = 'ERROR: cannot login'
        msg.fail = 1
        print (msg.appendMessage)
        ftp.quit()
        return msg
    print ('*** Logged in')


    try:
        ftp.cwd(DIRN)
    except ftplib.error_perm:
        msg.appendMessage = 'ERROR: cannot CD to "%s"' % DIRN
        msg.fail = 1
        print (msg.appendMessage)
        ftp.quit()
        return msg
    print ('*** Changed to "%s" folder' % DIRN)


    try:
        os.chdir(SAVELOC)
        ftp.retrbinary('RETR %s' % FILE,
        open(FILE, 'wb').write)
    except error_perm:
        os.unlink(FILE)
        msg.appendMessage = 'ERROR: cannot read file "%s"' % FILE
        msg.fail = 1
        print (msg.appendMessage)
        ftp.quit()
        return msg
    else:
        print ('*** Downloaded "%s" to CWD' % FILE)


    try:
        f.quit()
    except:
        pass
    msg.appendMessage = 'FTP transfer succeeded'
    return msg
