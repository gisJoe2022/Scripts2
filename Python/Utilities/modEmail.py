import os, sys
cmd_folder = "\\\\Nutsde\\GIS\\Production\\python\\CommonModules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import gbl, smtplib, string



def Send(Title, Message, Error, Recipient):

    SUBJECT = Title
    FROM = gbl.MyEmail
    text = Message

    if Recipient == None:
        TO = gbl.MyEmail
    else:
        TO = Recipient

    if Error == 0:

        BODY =  string.join((
                "From: %s" % FROM,
                "To: %s" % TO,
                "Subject: No errors in %s" % SUBJECT ,
                "",
                text
                ), "\r\n")
        server = smtplib.SMTP("smtp.co.washington.or.us")

        try:
            server.sendmail(FROM, TO.split(","), BODY)
        except:
            print "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])
        server.quit()

        print "\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2])

    else:

        try:

            BODY =  string.join((
                    "From: %s" % FROM,
                    "To: %s" % TO,
                    "Subject: ***ERROR*** %s" % SUBJECT ,
                    "",
                    text
                    ), "\r\n")
            server = smtplib.SMTP("smtp.co.washington.or.us")
            server.sendmail(FROM, TO.split(","), BODY)
            server.quit()

        except:

            BODY =  string.join((
                    "From: %s" % FROM,
                    "To: %s" % TO,
                    "Subject: ***ERROR*** %s" % SUBJECT ,
                    "",
                    "An error occured processing the error email"
                    ), "\r\n")
            server = smtplib.SMTP("smtp.co.washington.or.us")
            server.sendmail(FROM, TO.split(","), BODY)
            server.quit()




