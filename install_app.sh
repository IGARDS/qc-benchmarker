apt-get install -y redis-server
#pip install redis==2.10.6
source /data/env/bin/activate
pip install redis
pip install flask
pip install celery
pip install requests
pip install wheel
pip install blueprint
pip install Flask-BasicAuth
#apt install apache2

apt install -y apt-transport-https software-properties-common
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu xenial-cran35/'
apt update
apt -y purge r-base* r-recommended r-cran-*
apt -y autoremove
apt update
rm -rf /usr/local/lib/R/site-library/*
rm -rf /usr/lib/R/site-library/*
rm -rf /usr/lib/R/library/*
apt -y install libcurl3
apt -y install libpng-dev
apt -y install libreadline6 
apt -y install r-base* r-recommended

apt install -y libxml2-dev
apt install -y libnetcdf-dev
R -e 'install.packages("BiocManager",repos="http://cran.us.r-project.org")'
R -e 'BiocManager::install("mzR")'
R -e 'install.packages("knitr", repos="http://cran.us.r-project.org")'
R -e 'install.packages("rmarkdown", repos="http://cran.us.r-project.org")'
apt install -y pandoc
R -e 'install.packages("scales", repos="http://cran.us.r-project.org")'
R -e 'install.packages("XML", repos="http://cran.us.r-project.org")'
R -e 'BiocManager::install("pepXMLTab")'
R -e 'install.packages("Rcpp", repos="http://cran.us.r-project.org")'
R -e 'install.packages("plyr", repos="http://cran.us.r-project.org")'
R -e 'install.packages("rshape2", repos="http://cran.us.r-project.org")'
R -e 'install.packages("ggplot2", repos="http://cran.us.r-project.org")'
R -e 'BiocManager::install("MSnbase")'

#R -e 'library("rmarkdown"); render("/data/qc-benchmarker/qc_pipeline.Rmd","html_document")'

#cp index.html 


