import pandas as pd
import gspread
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Setup Google Sheets API Client
SERVICE_ACCOUNT_FILE = '/home/nineleaps/Documents/Patient_data_g_sheet_automation/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
docs_service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# Define the Spreadsheet ID and Sheet Name
spreadsheet_id = '12lnSOK8-viRaYAbDSQHOBUBb7sBHP6HI7O2t0s3IAMM'
sheet_name = 'patient_data'

# Load Data from Google Sheets into a Pandas DataFrame
spreadsheet = client.open_by_key(spreadsheet_id)
sheet = spreadsheet.worksheet(sheet_name)
data = sheet.get_all_records()
df = pd.DataFrame(data)

# 2. Filter the data to get the last five canceled appointments
cancelled_appointments = df[df['Status'].str.lower() == 'cancelled'].tail(5)

# 3. Prepare the email content
email_content = f"Here are the details of the last five cancelled appointments:\n\n{cancelled_appointments.to_string(index=False)}"

# 4. Email configuration
sender_email = input("Enter the sender mail : ")  
receiver_email = input("Enter the receiver mail : ")
subject = "Last Five Cancelled Appointments"
smtp_server = 'smtp.gmail.com' 
smtp_port = 587 
smtp_username = 'dhanush.venkataraman@nineleaps.com' 
smtp_password = 'bvtu imnj fwye wvlr' 

# 5. Create the email message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

# Attach the email content as plain text
message.attach(MIMEText(email_content, 'plain'))

# 6. Send the email
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email sent successfully to {receiver_email}")
except Exception as e:
    print(f"Failed to send email: {e}")
