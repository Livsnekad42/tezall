# gunicorn -c gunicorn.py main.wsgi&
gunicorn -c gunicorn.py main.asgi:application -k uvicorn.workers.UvicornWorker