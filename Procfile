web: gunicorn manage:app -w 3
worker: celery -A manage:celery_app worker --loglevel=info
