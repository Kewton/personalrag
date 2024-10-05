from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from app.schemas.ollama_chat import OllamaChat
from app.core.config import LOCUL_OLLAMA_URI
import requests

router = APIRouter()

@router.post("/ollama")
def use_ollama(request: OllamaChat):
    # 送信するデータ (例: JSON形式のデータ)
    data = {
        'model': request.model,
        'stream': request.stream,
        'messages': request.messages
    }

    try:
        # POSTリクエストの送信
        response = requests.post(f'http://{LOCUL_OLLAMA_URI}/api/chat', json=data)
        
        # ステータスコードの確認
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to connect to Ollama API")

        # レスポンスがJSON形式の場合に整形
        try:
            response_data = response.json()  # JSONとしてパース
        except ValueError:
            raise HTTPException(status_code=500, detail="Invalid response format")

        # 必要に応じてレスポンスを整形
        formatted_response = {
            "status_code": response.status_code,
            "data": response_data
        }

        return formatted_response

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
