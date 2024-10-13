import os.path
from app.core.config import GOOGLE_APIS_GMAIL_READONLY_TOKEN_PATH, GOOGLE_APIS_CREDENTIALS_PATH
from app.utils.logger import writedebuglog
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import html2text

# スコープ: Gmailの読み取り権限
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def convert_html_to_markdown(html_content):
    print("convert start")
    # html2textのインスタンスを作成
    converter = html2text.HTML2Text()

    # リンクを無視する
    converter.ignore_links = True
    # 画像を無視する
    converter.ignore_images = False
    # 幅制限を無効にする
    converter.body_width = 0

    # HTMLをMarkdownに変換
    markdown_content = converter.handle(html_content)
    return markdown_content


# Gmail APIサービスの認証と初期化
def create_gmail_service():
    creds = None
    if os.path.exists(GOOGLE_APIS_GMAIL_READONLY_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GOOGLE_APIS_GMAIL_READONLY_TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_APIS_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(GOOGLE_APIS_GMAIL_READONLY_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service


# 件名に指定されたキーワードが含まれるメールを検索し、本文を取得する関数
def get_emails_by_subject(subject_keyword):
    service = create_gmail_service()
    
    # メールを検索 (件名にキーワードを含む)
    query = f'subject:{subject_keyword}'
    results = service.users().messages().list(userId='me', q=query).execute()
    
    messages = results.get('messages', [])
    if not messages:
        print(f"No emails found with subject containing '{subject_keyword}'")
        return []

    email_bodies = []
    
    # メッセージIDを使ってメールの詳細を取得し、本文を抽出
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']
        
        # メール本文のパートを探す
        body_data = None
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain': # "text/html" "text/plain"
                    body_data = part['body']['data']
                    break
        else:
            body_data = payload['body']['data']

        if body_data:
            # Base64でエンコードされたデータをデコード
            body_decoded = base64.urlsafe_b64decode(body_data.encode('ASCII')).decode('utf-8')
            email_bodies.append({"email_body": convert_html_to_markdown(body_decoded)})
            # print(f"Email Body: {body_decoded}")
        else:
            print(f"Could not extract body from email with ID {message['id']}")

    # markdown_bodies = [convert_html_to_markdown(body) for body in email_bodies]
    # writedebuglog(markdown_bodies)
    print(len(email_bodies))
    return email_bodies

# get_emails_by_subject("週刊Life is beautiful ２０２４年１０月１日号")