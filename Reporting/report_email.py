""" 
This script will send a generated report (a file) via email.
 
"""


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

import report_fc_nulls

layer_name = report_fc_nulls.layer_name
output_excel = report_fc_nulls.output_excel
output_file = report_fc_nulls.output_file

def send_email(subject, body, to_emails, attachment_path):
    from_email = "youremail.com"
    from_password = "yourpassword"
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    
    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    with open(attachment_path, "rb") as attachment:
    attachment = open(attachment_path, "rb")
    
    # Instance of MIMEBase and named as p
    part = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    part.set_payload(attachment.read())
    
    # Encode into base64
    encoders.encode_base64(part)
    
    part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
    
    # Attach the instance 'part' to instance 'msg'
    msg.attach(part)
    
    # Create SMTP session for sending the mail
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)  # Use your SMTP server and port
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_emails, text)
    server.quit()

# Define email details
subject = "Null Values Report"
body = "Please find attached the null values report."
to_emails = ["jhayes@brwa.com"]
attachment_path = "null_values_report_your_feature_layer_name.xlsx"  # Update with the actual file name

# Send the email
send_email(subject, body, to_emails, attachment_path)

print("Email sent successfully!")