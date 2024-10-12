import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from app.schemas.vectorrag.vectordb_modelpath import VectorDBModelPath
from app.schemas.vectorrag.similarity_search import SimilaritySearchRequest
from app.schemas.vectorrag.git_path import GitPath
from app.schemas.vectorrag.recreate_vectorindex import RecreateVecorIndex
from app.services.db.task_result import get_task_status, create_task
from app.services.vectorindex.create_vectorindex import create_vectorindex, download_model, recreate_vectorindex
from app.services.exec_gitcommand import git_clone, git_pull
from app.services.db.reset_database import reset_database
from app.utils.url_operation import extract_last_segment
from app.services.vectorindex.llm import personalrag
from app.core.vectorindex.myVectorDBIndexies import MyVectorDB


router = APIRouter()


@router.post("/createVectorDatabase")
async def create_vector_database_task(request: VectorDBModelPath, background_tasks: BackgroundTasks):
    receipt_number = str(uuid.uuid4())
    create_task(receipt_number, "createVectorDatabase")  # タスクをデータベースに保存
    background_tasks.add_task(create_vectorindex, request.modelurl, receipt_number)
    return {"receipt_number": receipt_number}


@router.post("/reloadVectorDatabase")
def reloard_vectordb(request: VectorDBModelPath):
    _modelname = extract_last_segment(request.modelurl)
    if MyVectorDB.reload(_modelname):
        return {"message": "OK"}
    else:
        return {"message": "NG"}


@router.post("/reset-database")
def reset_db():
    try:
        reset_database()
        return {"message": "Database has been reset successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting database: {str(e)}")


@router.post("/similarity_search_with_score")
def similarity_search_with_score(request: SimilaritySearchRequest):
    _modelname = extract_last_segment(request.modelurl)
    if MyVectorDB.getindexstatus(_modelname):
        return MyVectorDB.similarity_search_with_score(_modelname, request.query)
    else:
        return {"message": "No vector database exists that can be loaded.After creating the vector database, please reload it."}


@router.post("/rag")
def rag(request: SimilaritySearchRequest):
    _modelname = extract_last_segment(request.modelurl)
    if MyVectorDB.getindexstatus(_modelname):
        similarity_search_result = MyVectorDB.similarity_search_with_score(_modelname, request.query)
        result = personalrag(request.query, similarity_search_result)
        return {
            "input_query": request.query,
            "similarity_search_result": similarity_search_result,
            "rag_result": result
            }
    else:
        return {"message": "No vector database exists that can be loaded.After creating the vector database, please reload it."}


@router.post("/download_model")
async def download_model_api(request: VectorDBModelPath, background_tasks: BackgroundTasks):
    receipt_number = str(uuid.uuid4())
    print(request.modelurl)
    create_task(receipt_number, "download_model")  # タスクをデータベースに保存
    background_tasks.add_task(download_model, request.modelurl, receipt_number)
    return {"receipt_number": receipt_number}


@router.post("/git_clone")
def git_clone_api(request: GitPath):
    return {"result": git_clone(request.githuburl)}


@router.post("/git_pull")
def git_pull_api(request: GitPath):
    return {"result": git_pull(request.githuburl)}


@router.post("/update_vectordatabase")
async def update_vectordatabase(request: RecreateVecorIndex, background_tasks: BackgroundTasks):
    receipt_number = str(uuid.uuid4())
    create_task(receipt_number, "recreate_database")  # タスクをデータベースに保存
    background_tasks.add_task(recreate_vectorindex, request.githuburl, request.modelurl, receipt_number)
    return {"receipt_number": receipt_number}

