import os, sys
#cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import gbl, smtplib, string


def Send(Title, Message, Error, Recipient):

    SUBJECT = Title
    FROM = gbl.MyEmailRyan
    # FROM = gbl.MyEmail
    text = Message

    if Recipient == None:
        TO = gbl.MyEmailRyan
    else:
        TO = Recipient

    if Error == 0:

        BODY = str.join('\r\n', ("From: {fname}".format(fname=FROM),
                               "To: {tname}".format(tname=TO),
                               "Subject: No errors in {sname}".format(sname=SUBJECT) ,
                               "",
                               text))
        server = smtplib.SMTP("smtp.co.washington.or.us")

        try:
            server.sendmail(FROM, TO.split(","), BODY)
        except:
            print ("\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2]))
        server.quit()

        print ("\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2]))

    else:

        try:
            BODY = str.join('\r\n', ("From: {fname}".format(fname=FROM),
                                   "To: {tname}".format(tname=TO),
                                   "Subject: ***ERROR*** {sname}".format(sname=SUBJECT),
                                   "",
                                   text))
            server = smtplib.SMTP("smtp.co.washington.or.us")
            server.sendmail(FROM, TO.split(","), BODY)
            server.quit()

        except:
            BODY = str.join('\r\n', ("From: {fname}".format(fname=FROM),
                                   "To: {tname}".format(tname=TO),
                                   "Subject: ***ERROR*** {sname}".format(sname=SUBJECT) ,
                                   "",
                                   "An error occurred processing the error email"))
            server = smtplib.SMTP("smtp.co.washington.or.us")
            server.sendmail(FROM, TO.split(","), BODY)
            server.quit()
