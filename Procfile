web: gunicorn --error-logfile '-' --log-file - --access-logfile '-' manage:app -w 4 --reload
worker: celery -A manage:celery_app worker --loglevel=info -c 1 --without-gossip --without-mingle --without-heartbeat
