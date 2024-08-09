import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gspread
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

# Convert Appointment_Date to datetime format
df['Appointment_Date'] = pd.to_datetime(df['Appointment_Date'], errors='coerce')

# 1. Distribution of Appointments by Status
plt.figure(figsize=(8, 6))
sns.countplot(y='Status', data=df, hue='Status', dodge=False, palette='viridis', legend=False)
plt.title('Distribution of Appointments by Status')
plt.xlabel('Number of Appointments')
plt.ylabel('Status')
plt.savefig('/home/nineleaps/Documents/Patient_data_g_sheet_automation/visualizations/appointments_by_status.png') 

# 2. Number of Appointments per Department
plt.figure(figsize=(10, 6))
sns.countplot(y='Department', data=df, hue='Department', dodge=False, palette='magma', order=df['Department'].value_counts().index, legend=False)
plt.title('Number of Appointments per Department')
plt.xlabel('Number of Appointments')
plt.ylabel('Department')
plt.savefig('/home/nineleaps/Documents/Patient_data_g_sheet_automation/visualizations/appointments_by_department.png') 

# 3. Appointments Over Time
plt.figure(figsize=(12, 6))
df['Appointment_Date'].value_counts().sort_index().plot(kind='line')
plt.title('Appointments Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Appointments')
plt.savefig('/home/nineleaps/Documents/Patient_data_g_sheet_automation/visualizations/appointments_over_time.png') 