import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

GOOGLE_APIS_GMAIL_SEND_TOKEN_PATH = 'token_gmail.json'
GOOGLE_APIS_CREDENTIALS_PATH = 'credentials.json' 


def send_email(service, to_email, subject, body):
    print("send_email 1")
    raw_msg = base64.urlsafe_b64encode(
        f"Subject: {subject}\nTo: {to_email}\n\n{body}".encode("utf-8")
    ).decode("utf-8")

    print("send_email 2")
    message = {"raw": raw_msg}
    service.users().messages().send(userId="me", body=message).execute()


def get_gmail_service():
    creds = None
    if os.path.exists(GOOGLE_APIS_GMAIL_SEND_TOKEN_PATH):
        with open(GOOGLE_APIS_GMAIL_SEND_TOKEN_PATH, 'r') as token_file:
            creds = Credentials.from_authorized_user_file(GOOGLE_APIS_GMAIL_SEND_TOKEN_PATH)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_APIS_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(GOOGLE_APIS_GMAIL_SEND_TOKEN_PATH, 'w') as token_file:
                token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


if __name__ == "__main__":
    service = get_gmail_service()
    send_email(
        service,
        "newtons.boiled.clock@gmail.com", 
        "test", 
        "testtest")