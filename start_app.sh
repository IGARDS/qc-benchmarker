#!/bin/bash
source /data/env/bin/activate
python --version
python app.py > /tmp/app.log 2>&1
