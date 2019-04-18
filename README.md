# QC Benchmarker

## Install instructions for a dev environment
These instructions are to configure a new dev environment. To run the project you need to follow
a few steps.

1. Install Docker
2. sudo docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
3. sudo docker run -p 443:9999 -p 80:7777 -it chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
4. git clone https://github.com/IGARDS/qc-benchmarker
5. cd qc-benchmarker
6. sudo ./install_dev.sh
7. sudo docker ps # copy the container id
8. sudo docker exec -it <container id> bash
9. Start whatever you want :)

## People
Magnus

Ben

Paul
