source env/bin/activate

# gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

uvicorn app:app --reload

