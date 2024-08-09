import gspread
import pandas as pd
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

# Generate Insights
def generate_insights(df):
    insights = []
    
    # Example insights
    total_appointments = len(df)
    completed_appointments = df[df['Status'].str.lower() == 'completed'].shape[0]
    cancelled_appointments = df[df['Status'].str.lower() == 'cancelled'].shape[0]
    avg_appointments_per_department = df.groupby('Department').size().mean()
    
    insights.append(f"Total Number of Appointments: {total_appointments}")
    insights.append(f"Number of Completed Appointments: {completed_appointments}")
    insights.append(f"Number of Cancelled Appointments: {cancelled_appointments}")
    insights.append(f"Average Number of Appointments per Department: {avg_appointments_per_department:.2f}")

    return "\n".join(insights)

# Create a new Google Doc and write insights
def create_doc_and_export_insights(insights):
    # Create the document
    doc = docs_service.documents().create(body={
        'title': 'Patient Data Insights'
    }).execute()

    document_id = doc.get('documentId')
    
    # Write the insights to the document
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1
                },
                'text': insights
            }
        }
    ]

    docs_service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    # Set the document permissions to allow anyone with the link to view it
    try:
        drive_service.permissions().create(
            fileId=document_id,
            body={
                'type': 'anyone',
                'role': 'reader',
            }
        ).execute()

        print(f"Insights have been written to Google Doc with ID: {document_id}")
        print(f"Link to view the document: https://docs.google.com/document/d/{document_id}/edit")

    except HttpError as error:
        print(f"An error occurred: {error}")
        print(f"Insights were created, but setting permissions failed. Document ID: {document_id}")

# Main execution
insights = generate_insights(df)
create_doc_and_export_insights(insights)
