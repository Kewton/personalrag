import os.path
from app.core.config import GOOGLE_APIS_GMAIL_SEND_TOKEN_PATH, GOOGLE_APIS_CREDENTIALS_PATH
from app.utils.logger import declogger, writeinfolog, writedebuglog, writeerrorlog
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def send_email(to_email, subject, body):
    try:
        service = get_gmail_service()

        # MIMEメッセージを作成
        message = MIMEMultipart()
        message['To'] = to_email
        message['From'] = "me"
        message['Subject'] = subject
        
        # メール本文を設定
        msg_body = MIMEText(body, "plain", "utf-8")
        message.attach(msg_body)

        # メッセージをbase64エンコード
        raw_msg = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        message_body = {"raw": raw_msg}

        # メールを送信
        service.users().messages().send(userId="me", body=message_body).execute()

        return True
    except HttpError as e:
        print(f"Standard HttpError: {e.stderr}")
        writeerrorlog(f"Standard HttpError: {e.stderr}")
        return False
    except Exception as e:
        print(f"Standard Exception: {e.stderr}")
        writeerrorlog(f"Standard Exception: {e.stderr}")
        return False


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
    #service = get_gmail_service()
    send_email(
        "newtons.boiled.clock@gmail.com", 
        "test", 
        "testtest")