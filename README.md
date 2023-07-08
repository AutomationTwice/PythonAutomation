# PythonAutomation
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import datetime
import sys

CREDENTIALS_DATA ={}


SPREADSHEET_ID = ''
api_key = ''

# Set the credentials and API key
credentials = ServiceAccountCredentials.from_json_keyfile_dict(CREDENTIALS_DATA)
api_service = build('youtube', 'v3', developerKey=api_key)

# Authenticate using the credentials
client = gspread.authorize(credentials)

# Open the spreadsheet
spreadsheet = client.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.sheet1

# Get the video IDs from the spreadsheet
video_ids = worksheet.row_values(3)[1:]
#print(video_ids)

# Define a function to get the YouTube view count for a video ID
def get_view_count(video_ids):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(part='statistics', id=video_ids)
    response = request.execute()
    items = response['items']
    if items:
        view_counts = [int(item['statistics']['viewCount']) for item in items]
        return view_counts
    else:
        return None

# Get the current date
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Find the next available row
next_row = len(worksheet.get_all_values()) + 1

# Update the spreadsheet with the current date and view count data in the next row
view_counts = get_view_count(video_ids)
data = [current_date] + view_counts
worksheet.insert_row(data, next_row)

# Script executed successfully
print("Script executed successfully.")
# Check if running in IPython environment and exit accordingly
if 'ipykernel' in sys.modules:
    quit()
else:
    sys.exit(0)
