# QC Benchmarker

## Install instructions for a dev environment
These instructions are to configure a new dev environment. To run the project you need to follow
a few steps.

1. Install Docker
2. sudo docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
3. sudo docker run -d -p 443:9999 -p 80:7777 -it chambm/pwiz-skyline-i-agree-to-the-vendor-licenses bash
7. sudo docker ps # copy the container id
4. sudo docker exec -it <container id> bash # After this you will be inside the container
4. apt update
4. apt install -y git
4. git clone https://github.com/IGARDS/qc-benchmarker
5. cd qc-benchmarker
6. ./install_dev.sh
7. ./install_app.sh
9. Start whatever you want :)

## People
Magnus

Ben

Paul
