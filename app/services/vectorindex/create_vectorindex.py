from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
from app.utils.run_shell_command import run_shell_command
from app.utils.url_operation import extract_last_segment
from app.utils.dir_operation import remove_directory_if_exists
from app.services.db.task_result import update_task, close_task
from app.core.config import INDEX_SAVE_DIR, MODEL_DOWNLOAD_DIR, DOC_DOWNLOAD_DIR
from app.core.vectorindex.ragindexhelper import createDocuments
from app.services.exec_gitcommand import git_clone
from app.core.vectorindex.myVectorDBIndexies import MyVectorDB
from app.utils.logger import declogger, writeinfolog, writedebuglog


@declogger
def create_vectorindex(modelurl: str, task_id: str):
    _doc_dir = DOC_DOWNLOAD_DIR
    _model_path = os.path.join(MODEL_DOWNLOAD_DIR, extract_last_segment(modelurl))
    _save_path = os.path.join(INDEX_SAVE_DIR, extract_last_segment(modelurl))

    _remarks = "Processed directory: " + _doc_dir + ";" + _model_path
    update_task(task_id, _remarks)
    try:
        documents = createDocuments(_doc_dir)
        index = FAISS.from_documents(
            documents=documents,
            embedding=HuggingFaceEmbeddings(model_name=_model_path),
        )
        index.save_local(_save_path)
        close_task(task_id, "success", _remarks)
    except Exception as e:
        close_task(task_id, "abnormalend", e)


@declogger
def download_model(githuburl: str, task_id: str):
    print("download_model start")
    _remarks = "download_model"
    update_task(task_id, _remarks)
    try:
        _path = os.path.join(MODEL_DOWNLOAD_DIR, extract_last_segment(githuburl))
        remove_directory_if_exists(_path)
        run_shell_command("git lfs install")
        run_shell_command(f"git clone {githuburl} {_path}")
        close_task(task_id, "success", _remarks)
    except Exception as e:
        close_task(task_id, "abnormalend", e)


@declogger
def recreate_vectorindex(githuburl: str, modelurl: str, task_id: str):
    try:
        _doc_dir = DOC_DOWNLOAD_DIR
        _model_path = os.path.join(MODEL_DOWNLOAD_DIR, extract_last_segment(modelurl))
        _save_path = os.path.join(INDEX_SAVE_DIR, extract_last_segment(modelurl))

        update_task(task_id, "git_clone start")
        git_clone(githuburl)

        update_task(task_id, "create index: " + _doc_dir + ";" + _model_path)
        documents = createDocuments(_doc_dir)
        index = FAISS.from_documents(
            documents=documents,
            embedding=HuggingFaceEmbeddings(model_name=_model_path),
        )
        update_task(task_id, "save index")
        index.save_local(_save_path)

        update_task(task_id, "reload index")
        _modelname = extract_last_segment(modelurl)
        MyVectorDB.reload(_modelname)

        close_task(task_id, "success", _doc_dir + ";" + _model_path)
    except Exception as e:
        close_task(task_id, "abnormalend", e)
