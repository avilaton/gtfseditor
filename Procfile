web: gunicorn --error-logfile '-' --log-file - --access-logfile '-' manage:app -w 4 --reload -b 0.0.0.0:5000
worker: celery -A manage:celery_app worker --loglevel=info -c 1 --without-gossip --without-mingle --without-heartbeat
