source /data/env/bin/activate
nohup jupyter lab  --ip=0.0.0.0 --port=9999 --allow-root > /var/log/jupyter.log 2>&1 &
