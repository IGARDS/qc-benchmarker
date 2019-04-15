nohup celery -A app.celery worker > /var/log/celery.log 2>&1 &
