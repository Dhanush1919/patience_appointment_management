import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# 1. Setup Google Sheets API Client
SERVICE_ACCOUNT_FILE = '/home/nineleaps/Documents/Patient_data_g_sheet_automation/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 2. Define the Spreadsheet ID and Sheet Name
spreadsheet_id = '12lnSOK8-viRaYAbDSQHOBUBb7sBHP6HI7O2t0s3IAMM'
sheet_name = 'patient_data'

# 3. Load Data from Google Sheets into a Pandas DataFrame
spreadsheet = client.open_by_key(spreadsheet_id)
sheet = spreadsheet.worksheet(sheet_name)
data = sheet.get_all_records()

df = pd.DataFrame(data)

# 4. Preview the Data
print("Initial Data Preview:")
print(df.head())

# 5. Check for Missing Values
print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# 6. Handle Missing Values
df['Doctor'] = df['Doctor'].fillna('Unknown')  # Fill missing values in 'Doctor' column

# 7. Convert Data Types
df['Appointment_Date'] = pd.to_datetime(df['Appointment_Date'], errors='coerce', dayfirst=True)

# 8. Remove Duplicates
df = df.drop_duplicates()

# 9. Standardize Text Columns
df['Patient_Name'] = df['Patient_Name'].str.title()
df['Doctor'] = df['Doctor'].str.title()

# 10. Sort the Data (Optional)
df = df.sort_values(by=['Appointment_Date', 'Appointment_Time'])

# 11. Reset Index After Cleaning
df = df.reset_index(drop=True)

# Convert all date columns to string format
df['Appointment_Date'] = df['Appointment_Date'].dt.strftime('%Y-%m-%d')

# 12. Replace Infinite Values and NaNs
df.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
df.fillna('Unknown', inplace=True)

# 13. Handling appointment_time value :
df = df.dropna(subset=['Appointment_Time'])  # Remove rows where 'Appointment_Time' is NaN

# 13. Final Preview of Cleaned Data
print("\nCleaned Data Preview:")
print(df.head())

# 14. Write the Cleaned Data Back to Google Sheets
# Clear the existing data in the sheet
sheet.clear()

# Convert DataFrame to list of lists and update the sheet
data_to_write = [df.columns.values.tolist()] + df.values.tolist()
sheet.update(data_to_write)

print("Cleaned data has been written back to Google Sheets.")
