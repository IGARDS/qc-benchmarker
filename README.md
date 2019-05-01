# QC Benchmarker

## Install instructions for a new dev environment
These instructions are to configure a new dev environment. To run the project you need to follow
a few steps.

1. Install Docker
2. sudo docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
3. sudo docker run -d -p 9999:9999 -p 7777:7777 -it chambm/pwiz-skyline-i-agree-to-the-vendor-licenses bash
7. sudo docker ps # copy the container id
4. sudo docker exec -it <container id> bash # After this you will be inside the container
4. apt update
4. apt install -y git
4. git clone https://github.com/IGARDS/qc-benchmarker
5. cd qc-benchmarker
6. ./install_dev.sh
7. ./install_app.sh
9. Start whatever you want :)
  
## Install using a previous container
1. Install docker
2. sudo docker pull pauleanderson/qc-benchmarker
3. sudo docker run -d -p 9999:9999 -p 7777:7777 -p 8787:8787 -it pauleanderson/qc-benchmarker
4. Start whatever you want :)

## Port notes
9999 is jupyter lab

7777 is the flask server

8787 is rstudio

## People
Magnus

Ben

Paul
