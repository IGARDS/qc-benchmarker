#!/bin/bash
source /data/env/bin/activate
nohup jupyter lab  --ip=0.0.0.0 --port=9999 --allow-root  --LabApp.base_url=jupyter > /tmp/jupyter.log 2>&1 &
