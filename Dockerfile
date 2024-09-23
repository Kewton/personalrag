# Python 3.11をベースにする
FROM python:3.11-slim

# 必要なパッケージをインストールし、gitを追加
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    git-lfs \
    && git lfs install \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# アップロードフォルダを作成
RUN mkdir -p /usr/share/uploads

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Flaskアプリケーションを実行
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
