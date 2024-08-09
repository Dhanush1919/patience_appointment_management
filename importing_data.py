#### THE BELOW SET OF CODE TAKES THE DATA FROM CSV AND IMPORTS IT INTO THE GIVEN SHEET 

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import schedule
import time

# 1. Setup Google Sheets API Client
SERVICE_ACCOUNT_FILE = '/home/nineleaps/Documents/Patient_data_g_sheet_automation/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 2. Define the Spreadsheet ID and Sheet Name
spreadsheet_id = '12lnSOK8-viRaYAbDSQHOBUBb7sBHP6HI7O2t0s3IAMM'
sheet_name = 'patient_data'

# 3. Function to Import CSV Data to Google Sheets
def import_csv_to_gsheet(csv_file, batch_size=100):
    # Access the Google Sheet
    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.worksheet(sheet_name)
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Convert DataFrame to list of lists for gspread
    data = df.values.tolist()
    
    # Append headers if the sheet is empty
    if not sheet.get_all_values():
        headers = df.columns.tolist()
        sheet.append_row(headers)
    
    # Batch insertion
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        sheet.append_rows(batch)
        time.sleep(1)  # Add a short delay to avoid hitting the rate limit

    print(f"Data from {csv_file} imported successfully to {sheet_name}.")

# 4. Schedule the Import Task
def schedule_import(csv_file, import_time):
    schedule.every().day.at(import_time).do(import_csv_to_gsheet, csv_file=csv_file)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait one minute between checks

# 5. Main Function to Run the Automation
if __name__ == "__main__":
    csv_file_path = '/home/nineleaps/Documents/Patient_data_g_sheet_automation/appointments.csv'

    import_time = input('Enter the time to import (e.g., "14:30" for 2:30 PM): ')
    
    schedule_import(csv_file_path, import_time)
    
    print("Scheduled CSV import task is now running. Press Ctrl+C to stop.")
