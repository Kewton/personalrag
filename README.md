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
SQLALCHEMY_DATABASE_URL=sqlite:///<>/test.db
PROJECT_ROOT_DIRECTORY=<>
```