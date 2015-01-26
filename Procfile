web: gunicorn manage:app -w 3
worker: celery -A app.tasks worker --loglevel=info