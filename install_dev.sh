#!/bin/bash 
apt update
apt install -y vim
apt install -y curl

add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.6

# Get the pip install program
PIP_SCRIPT=/tmp/get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o $PIP_SCRIPT
chmod +x $PIP_SCRIPT

# Install it for python3
python3.6 $PIP_SCRIPT --user
$HOME/.local/bin/pip3.6 install virtualenv

ENV_DIR=/data/env
python3.6 -m virtualenv $ENV_DIR
source $ENV_DIR/bin/activate

pip install jupyter
pip install jupyterlab

#apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
#echo "deb https://cloud.r-project.org/bin/linux/ubuntu xenial-cran35/" >> /etc/apt/sources.list
#apt-get install -y r-base r-base-dev

#echo "deb http://cran.rstudio.com/bin/linux/debian jessie-cran3/" >> /etc/apt/sources.list
#apt-get update
#apt install -y dirmngr
#apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
#apt update
#apt install -y --force-yes r-base
#apt-get install r-cran-ncdf4

#dpkg --add-architecture i386 && apt update

#apt install \
#      wine \
#      wine32 \
#      wine64 \
#      libwine \
#      libwine:i386 \
#      fonts-wine
