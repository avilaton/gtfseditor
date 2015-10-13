web: gunicorn manage:app -w 1
worker: celery -A manage:celery_app worker --loglevel=info -c 1 --without-gossip --without-mingle --without-heartbeat
