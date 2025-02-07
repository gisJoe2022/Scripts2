""" queries all the field in a fc and reports the number 
    of null values to a spreadsheet with the fc name at
    the end of the fielname.

    this version emails the spreadhseet report.
      
    Author: Joe Hayes
    Date: 2/6/2025 """


""" must rember to install

    pip install arcgis pandas openpyxl

    Replace "your_username", "your_password", 
    "your_feature_layer_url", "your_email@example.com", 
    "your_email_password", and "smtp.example.com" with 
    your actual AGOL credentials, email credentials, and 
    SMTP server details. Also, update the to_emails list 
    with the email addresses of the recipients.
     
    """
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

# Connect to AGOL
gis = GIS("https://www.arcgis.com", "your_username", "your_password")

# Access the hosted feature layer
feature_layer_url = "your_feature_layer_url"
feature_layer = FeatureLayer(feature_layer_url)

# Query all features
features = feature_layer.query(where="1=1", out_fields="*").features

# Extract field names
field_names = [field['name'] for field in feature_layer.properties.fields]

# Initialize a dictionary to store null counts
null_counts = {field: 0 for field in field_names}

# Count null values for each field
for feature in features:
    for field in field_names:
        if feature.attributes[field] is None:
            null_counts[field] += 1

# Convert the dictionary to a DataFrame
df = pd.DataFrame(list(null_counts.items()), columns=['Field', 'Null Count'])

# Get the feature layer name
feature_layer_name = feature_layer.properties.name

# Save the DataFrame to an Excel file with the feature layer name
file_name = f"null_values_report_{feature_layer_name}.xlsx"
df.to_excel(file_name, index=False)

print(f"Report created successfully as {file_name}!")

# Email the report
def send_email(subject, body, to_emails, attachment_path):
    from_email = "your_email@example.com"
    from_password = "your_email_password"
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    
    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # Open the file to be sent
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
    server = smtplib.SMTP('smtp.example.com', 587)  # Use your SMTP server and port
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_emails, text)
    server.quit()

# Define email details
subject = "Null Values Report"
body = "Please find attached the null values report."
to_emails = ["recipient1@example.com", "recipient2@example.com"]

# Send the email
send_email(subject, body, to_emails, file_name)

print("Email sent successfully!")