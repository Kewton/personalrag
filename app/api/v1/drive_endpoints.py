from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from app.core.googleapis.drive import get_or_create_folder, upload_file, get_file_id_and_mime_type, download_file, list_files_in_folder_recursive, get_folder_id
from app.schemas.drive.googledrive import DownloadFile, GetId, UploadFile
from app.utils.logger import declogger, writeinfolog, writedebuglog, writeerrorlog
from app.utils.dir_operation import ensure_directory_exists
from app.core.config import PROJECT_ROOT_DIRECTORY
import os

router = APIRouter()

# ファイル一覧の取得
@router.get("/drive/list")
def get_fiilelist():
    file_list = []
    list_files_in_folder_recursive(get_folder_id("myapp"), "/myapp", file_list)
    return {"result": file_list}


@router.post("/drive/id")
def get_id(request: GetId):
    name, id, mimeType= get_file_id_and_mime_type(request.path)
    _l = [
        {
            "name": name,
            "id": id,
            "mimeType": mimeType,
            "path": request.path
        }
    ]
    return {"result": _l}


# ファイルダウンロード
@router.post("/drive/download2local")
def download_fiile(request: DownloadFile):
    full_path = os.path.join(PROJECT_ROOT_DIRECTORY, "googledrive", request.path.lstrip('/'))
    print(request.path)
    print(full_path)
    ensure_directory_exists(os.path.dirname(full_path))
    download_file(request.id, full_path)
    return {"result": "success", "path": full_path}


# ローカルファイルをアップロード
@router.post("/drive/upload2dribe")
def upload_fiile(request: UploadFile):
    try:
        id = upload_file(request.name, request.local_path, request.mimeType, get_or_create_folder(request.upload_path))
        _l = [
            {
                "name": request.name,
                "id": id,
                "mimeType": request.mimeType,
                "path": os.path.join(request.upload_path, request.name)
            }
        ]
        return {"result": _l}
    except Exception as e:
        print(e)
        writeerrorlog(e)
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")