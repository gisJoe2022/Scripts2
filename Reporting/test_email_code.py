

import smtplib
import os
import glob
import requests
import msal
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

def get_most_recent_file(folder_path, file_extension="*.*"):
    """Finds the most recent file in the specified folder with the given extension."""
    list_of_files = glob.glob(os.path.join(folder_path, file_extension))
    if not list_of_files:
        return None
    return max(list_of_files, key=os.path.getctime)

def get_access_token():
    """Gets an OAuth2 access token for Microsoft Graph API."""
    CLIENT_ID = "your_client_id"
    CLIENT_SECRET = "your_client_secret"
    TENANT_ID = "your_tenant_id"
    
    app = msal.ConfidentialClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", client_credential=CLIENT_SECRET)
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token.get("access_token")

def send_email(subject, body, to_emails, attachment_path):
    """Sends an email with an attachment using Microsoft Graph API."""
    access_token = get_access_token()
    if not access_token:
        print("Failed to obtain access token.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": body
            },
            "toRecipients": [
                {"emailAddress": {"address": to_emails[0]}}
            ]
        },
        "saveToSentItems": "true"
    }
    
    files = {"file": open(attachment_path, "rb")} if attachment_path else None
    response = requests.post("https://graph.microsoft.com/v1.0/me/sendMail", json=email_data, headers=headers, files=files)
    
    if response.status_code == 202:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email: {response.text}")

# Define email details
folder_path = "C:/path/to/your/folder"  # Update with the actual folder path
subject = "Null Values Report"
body = "Please find attached the most recent null values report."
to_emails = ["jhayes@brwa.com"]

# Get the most recent file
recent_file = get_most_recent_file(folder_path, "*.xlsx")
if recent_file:
    send_email(subject, body, to_emails, recent_file)
else:
    print("No recent file found to send.")