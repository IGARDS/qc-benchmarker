redis-server >/var/log/redis.log 2>&1 &

celery -A app.celery worker > /var/log/celery.log 2>&1 &

python app.py > /var/log/app.log 2>&1 &



