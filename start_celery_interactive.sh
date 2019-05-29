celery -A app.celery worker -f /var/log/celery.log --concurrency 1 -l INFO
