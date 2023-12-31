import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import datetime
import sys
import pytz

CREDENTIALS_DATA = {
  "type": "service_account",
  "project_id": "python-automation-391415",
  "private_key_id": "9d4c173e073c608f0a89e1c9c669d70a29e2d64d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDbOm0m9Ko0whTf\nz2AkYbekMjIPLMOEyJXILGekB6beMmZMm8Mao8vfpfsFK7vZ+UWfOmsthVFnFgFI\nBjEnXxOSsgTpBQXmLANi9KsDyadbrTPhCoFSsfDe8zVVRQmKh2TqOwJwmUTF5O39\nrY0lDEVximYSYeobfyPJ3DDygjLw7uwnPwpa0chV4Q96CjN+Vcw9yA/G7/GIeISD\nYRKCOCS3WXTHcp//JPNCsA7xKoIb8JIuZIQ/xLG3Ely3JRFCaGLbKSDz4Gk9bKq4\nptJS6200AX4nHxGIsJd4pyrHBCsVnNgHaYE24KBNbZYyMvXO331xNCyBrFPU8OcB\ntPGpavgdAgMBAAECggEACMKW/dqVHtlKP4gafJv4boq7zBGUNIFV+k6COWmG3PiO\nvciBmx9ET8kHWVDC2dGVNo2PsPicwFJHtdPbOopP17LeXzfnhcxolWCgM10waHcx\n+gIuhuNXhlJQnDEGP6Y1PZ1sLHb0j1pllZdgRmk2MOJb9IMXQocFR7m+9q5hopWp\n8vNmQ9D2pudmAd4Esh9p0bk2lWG6m02afST0TML+ud1Ld652WDDY572jOGjF7Qwy\nF7kxgLWmZBsP4PP7PH7XLdneCQGjJmeS5uWbzJhGeJCnwIKkWJCX3kiQfS4/A48V\n8iJzZVRKeL+YsHEDhIiQlrNrNS2ytKu/BWltXs9XvwKBgQD+6ytS8CU5/nP2A1f8\nPfmSBVTN2gWa3wsEPZoV3AbLPkf1xIR0iAFupfjsbIPUTRcMd3P41ApRPBbwn1Sn\nej/gAukGdaMsHnTd1K8jBaUu/aWNPmvARXRoHk8sjt6PUjBwd4Cd/DrB6VAbeyiy\nc56HkZIZrbpZD02A1VJdw3Pf3wKBgQDcKH+3BL+2UL721ROJ+TRpbEOpoKLBQPg+\nOL8aJKb4oAy4+cMeunA9T+O41Uy/C16GihrX8djlBLsWPAoDsViIpHaper68NKXS\n1eH8IazdmM6pJb64T7Rv+y244ULsSKsF9b7wz4Zcs3Gf8SuveBjyF0wHqtWbYfl7\nVDRVNsm3gwKBgD/1SxJtFDn/wKJ55kpwVjyvv75CNGPOEFqJBi7z3HSD9NQR8VW3\nhfx4AgN3mn/as6y6D8vfj5MgK3VF1JyMjJgswsCPJVh9b770jNiRowcuNqpAfhJo\nmrNA34aDdg2phmPBZ/C7hxZ97k5m0Sgs4BqNiIWO1BFiSITJgPfrgRgrAoGAPHo3\nkzwPufJ2cvHXezhk6GzgLXG+I95IEzedb34QDA5TUGDz87X9bSpMARM/EN/7qHO5\nqgZ6sXbaOeJmUdte2bJsEmRwjtzbjI5KlOtfRERcyORgftsOUxCp37apnqTbrjhy\nqk4nt8FnfitO99XC7IXv0c9g/F0unm1kLuBtCycCgYEA4/u0nNFuishOReNa5QmI\nm/ypOC1fSWnUGPiAfpshm8XBCvxxt8zm/EVz7ofp9gdfFXqZQov2YHxzUTTR9l3Y\nd/qGoLnxfII+qmfdyiorCij7iBC8vsq5We9EXO5y+5/i5jYJ0X7ulooMpbsSQ2yy\nbLuevKGfJ0eQsY714APuSu0=\n-----END PRIVATE KEY-----\n",
  "client_email": "python-automation@python-automation-391415.iam.gserviceaccount.com",
  "client_id": "114268018686011779217",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-automation%40python-automation-391415.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


SPREADSHEET_ID = '1Oq4BG3EWmm3n0w4PiRJdPnNJCZeAbxgsV-LklArSYKM'
api_key = 'AIzaSyD-e60nOQwX4yUeA-YoEs89DL59PMV1uhY'

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

# Get the current date and time in Indian timezone
indian_timezone = pytz.timezone('Asia/Kolkata')
current_date = datetime.datetime.now(indian_timezone).strftime('%Y-%m-%d %H:%M:%S')

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
