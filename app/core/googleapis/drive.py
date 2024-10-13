from app.core.config import GOOGLE_APIS_DRIVE_TOKEN_PATH, GOOGLE_APIS_CREDENTIALS_PATH
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import io

# スコープ: 読み取り/書き込み
SCOPES = ['https://www.googleapis.com/auth/drive']


# 認証プロセス
def authenticate():
    creds = None
    if os.path.exists(GOOGLE_APIS_DRIVE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GOOGLE_APIS_DRIVE_TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_APIS_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(GOOGLE_APIS_DRIVE_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return creds


# Google Drive APIサービスの初期化
def create_service():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    return service


def upload_file(file_name, file_path, mime_type, folder_id=None):
    """
	- textファイル
        'text/plain'
    - PDFファイル (.pdf):
	    mime_type = 'application/pdf'
	- MP4ファイル (.mp4):
	    mime_type = 'video/mp4'
	- JPEGファイル (.jpg):
	    mime_type = 'image/jpeg'
	- Excelファイル (.xlsx):
	    mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    """
    service = create_service()

    # フォルダIDを指定した場合にメタデータに親フォルダを設定
    if folder_id:
        file_metadata = {'name': file_name, 'parents': [folder_id]}
    else:
        file_metadata = {'name': file_name}

    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"File ID: {file.get('id')}")
    return file.get('id')

# Resumable Uploadを実行する関数
def resumable_upload(file_name, file_path, mime_type, folder_id=None):
    service = create_service()

    # アップロードするファイルのメタデータ
    # フォルダIDを指定した場合にメタデータに親フォルダを設定
    if folder_id:
        file_metadata = {'name': file_name, 'parents': [folder_id]}
    else:
        file_metadata = {'name': file_name}

    # Resumable Uploadの準備
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

    # アップロード開始
    request = service.files().create(body=file_metadata, media_body=media, fields='id')

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Upload Complete. File ID: {response.get('id')}")


# フォルダが存在しなければ作成し、フォルダIDを返却する関数
def get_or_create_folder(folder_path):
    service = create_service()

    # パスを分割して処理 (例えば "./mywork/myapp/テスト" を ['mywork', 'myapp', 'テスト'] に分割)
    folder_names = folder_path.strip("./").split('/')

    # ルートフォルダから開始 (Google Driveのルートフォルダは'root'と指定)
    parent_id = 'root'

    # 各フォルダ名を順に処理し、フォルダが存在するか確認する
    for folder_name in folder_names:
        query = f"'{parent_id}' in parents and name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        if files:
            # フォルダが存在する場合、そのフォルダIDを取得して次の階層に進む
            parent_id = files[0]['id']
        else:
            # フォルダが存在しない場合、フォルダを作成する
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]  # 親フォルダのIDを指定
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            parent_id = folder['id']  # 作成したフォルダのIDを取得

    # 最後のフォルダIDを返す（これが最下層のフォルダ）
    return parent_id


def download_file(file_id, destination_path):
    service = create_service()
    
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')
    
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")


def get_folder_id(folder_name):
    service = create_service()

    # フォルダを検索するためのクエリ
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    
    results = service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print(f"No folder found with the name '{folder_name}'")
        return None
    else:
        # 複数のフォルダが見つかった場合は最初のフォルダIDを返す
        folder_id = items[0]['id']
        print(f"Folder ID for '{folder_name}': {folder_id}")
        return folder_id


def get_folder_id_by_path(folder_path):
    service = create_service()

    # フォルダのパスを"/"で分割して各フォルダを順に検索
    folder_names = folder_path.split('/')
    parent_id = 'root'  # 最初は「マイドライブ」から始める

    for folder_name in folder_names:
        # フォルダ名と親IDを使ってフォルダを検索するクエリ
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and '{parent_id}' in parents"
        
        results = service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print(f"No folder found with the name '{folder_name}' in the current path.")
            return None
        else:
            # 最初に見つかったフォルダIDを次の親フォルダとして設定
            parent_id = items[0]['id']
            print(f"Found folder '{folder_name}' with ID: {parent_id}")

    # 最後に見つかったフォルダのIDを返す
    return parent_id


def list_files_in_folder_recursive(folder_id, current_path, file_list):
    """
    フォルダ内のファイルとサブフォルダを再帰的に取得しリストに格納
    """
    service = create_service()
    query = f"'{folder_id}' in parents"
    results = service.files().list(
        q=query,
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()

    files = results.get('files', [])

    if not files:
        return

    # ファイルをリストに追加
    for file in files:
        # ファイルのフルパスを作成
        full_path = os.path.join(current_path, file['name'])
        
        # ファイル情報をリストに追加
        file_list.append({
            'name': file['name'],
            'id': file['id'],
            'mimeType': file['mimeType'],
            'path': full_path
        })
        
        # MIMEタイプがフォルダの場合、再帰的にサブフォルダ内のファイルを取得
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            list_files_in_folder_recursive(file['id'], full_path, file_list)


def get_file_id_and_mime_type(folder_path):
    """
    指定されたパスに基づいて、ファイルまたはフォルダのIDとmimeTypeを取得
    """
    service = create_service()

    # パスを分割 (例えば "./mywork/myapp/テスト/filename.pdf" を ['mywork', 'myapp', 'テスト', 'filename.pdf'] に分割)
    folder_names = folder_path.strip("./").split('/')

    # ルートフォルダから開始 (Google Driveのルートフォルダは'root'と指定)
    parent_id = 'root'

    # 各フォルダ/ファイル名ごとにDrive APIを使用して次の階層に進む
    for name in folder_names:
        query = f"'{parent_id}' in parents and name='{name}' and trashed=false"
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType)"
        ).execute()

        files = results.get('files', [])

        if not files:
            print(f"'{name}' not found in the specified path.")
            return None

        # 現在のフォルダ/ファイルの情報を取得
        file_info = files[0]
        parent_id = file_info['id']  # 次の階層に進むためのフォルダIDを更新

    # 最後に見つかったファイル/フォルダのIDとmimeTypeを返す
    return file_info['name'], file_info['id'], file_info['mimeType']


def list_files_in_folder(folder_id):
    service = create_service()

    # フォルダ内のファイルを検索するためのクエリ
    query = f"'{folder_id}' in parents"
    
    results = service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print(f"No files found in folder with ID '{folder_id}'")
        return []
    else:
        print(f"Files in folder with ID '{folder_id}':")
        for item in items:
            print(f"Name: {item['name']}, ID: {item['id']}")
        return items

# resumable_upload
# upload_file("000009974_loc2cloud_2myapp-2.pdf", "./000009974_loc.pdf", "application/pdf", get_folder_id("myapp"))
# resumable_upload("000009974_loc2cloud_2myapp-2.pdf", "./000009974_loc.pdf", "application/pdf", get_folder_id("myapp"))
# list_files_in_folder(get_folder_id("myapp"))
# download_file("1LPz4fYlAFdWbn3LwEKs4s9sMP2nIOY1x", "./000009974_loc.pdf")