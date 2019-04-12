apt-get update
apt-get install -y vim
pip install jupyter
pip install jupyterlab

echo "deb http://cran.rstudio.com/bin/linux/debian jessie-cran3/" >> /etc/apt/sources.list
apt-get update
apt install -y dirmngr
apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
apt update
apt install -y --force-yes r-base
apt-get install r-cran-ncdf4

dpkg --add-architecture i386 && apt update

apt install \
      wine \
      wine32 \
      wine64 \
      libwine \
      libwine:i386 \
      fonts-wine