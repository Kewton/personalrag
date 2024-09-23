# setup
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# exec
```
uvicorn app.main:app --reload
```

# .env
```

```

# docker build/raspberry pi
```
docker build --platform linux/arm64 -t <dockerhubuser>/rag_api_arm64:v0.1.1 . --no-cache
docker push <dockerhubuser>/rag_api_arm64:v0.1.1

docker build --platform linux/arm64 -t mynoo/rag_api_arm64:v0.1.4 . --no-cache
docker push mynoo/rag_api_arm64:v0.1.4
```
docker build -t mynoo/rag_api_mac:v0.1.3 . --no-cache
cd mywork
docker compose up
#docker run -d -p 8000:8000 mynoo/rag_api_mac:v0.1.3
docker exec -it 1f0e237c9e05 /bin/bash
curl http://127.0.0.1:8000/v1/

curl http://192.168.11.8:31953/rag-api/v1/
# doc
http://127.0.0.1:8000/redoc

http://127.0.0.1:8000/docs
https://aa60-210-237-99-225.ngrok-free.app/rag-api/docs

	•	kubectl get pods でポッドを確認
	•	kubectl exec -it <ポッド名> -- /bin/bash でログイン


curl http://127.0.0.1:8000/v1/check-task/93bcf4e4-8437-467a-8fc5-1297094d3fbe

curl -X POST "https://7b73-210-237-99-225.ngrok-free.app/v1/download_model" \
    -H "Content-Type: application/json" \
    -d '{"modelurl": "https://huggingface.co/intfloat/multilingual-e5-large"}'
{"receipt_number":"1eefb9f7-d261-495a-bb97-3c73b717c80a"}%                    


curl https://aa60-210-237-99-225.ngrok-free.app/rag-api/v1/check-task/1eefb9f7-d261-495a-bb97-3c73b717c80a
curl https://7b73-210-237-99-225.ngrok-free.app/v1/check-task/1eefb9f7-d261-495a-bb97-3c73b717c80a

curl http://192.168.11.8:31953/rag-api/v1/