apt-get install -y redis-server
#pip install redis==2.10.6
source /data/env/bin/activate
pip install redis
pip install flask
pip install celery
pip install requests
pip install blueprint
#apt install apache2

apt install libnetcdf-dev
R -e 'BiocManager::install("mzR")'
R -e 'install.packages("knitr")'
R -e 'install.packages("rmarkdown")'
apt install -y pandoc
R -e 'install.packages("scales")'

#R -e 'library("rmarkdown"); render("/data/qc-benchmarker/qc_pipeline.Rmd","html_document")'

#cp index.html 


