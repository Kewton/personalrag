import os.path
from app.core.config import GOOGLE_APIS_TOKEN_PATH, GOOGLE_APIS_CREDENTIALS_PATH
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/drive'
]


def get_googleapis_service(_serviceName):
    creds = None
    if os.path.exists(GOOGLE_APIS_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GOOGLE_APIS_TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_APIS_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(
                port=0,
                authorization_url_params={
                    'access_type': 'offline',
                    'prompt': 'consent'
                }
            )
            with open(GOOGLE_APIS_TOKEN_PATH, 'w') as token_file:
                token_file.write(creds.to_json())

    if _serviceName == "gmail":
        return build('gmail', 'v1', credentials=creds)
    elif _serviceName == "drive":
        return build('drive', 'v3', credentials=creds)
    else:
        return None
