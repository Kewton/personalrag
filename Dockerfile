# Python 3.11をベースにする
FROM python:3.11-slim

# アップロードフォルダを作成
RUN mkdir -p /usr/share/uploads

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Flaskアプリケーションを実行
CMD ["uvicorn", "app.main:app", "--reload"]
