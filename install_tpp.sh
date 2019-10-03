# http://tools.proteomecenter.org/wiki/index.php?title=TPP_5.1.0:_Installing_on_Ubuntu_16.04_LTS

apt update
apt --yes upgrade
apt --yes install subversion
apt --yes install make
apt --yes install g++
apt --yes install build-essential
apt --yes install zlib1g-dev
apt --yes install libghc-bzlib-dev
apt --yes install gnuplot
apt --yes install unzip
apt --yes install expat
apt --yes install libexpat1-dev
apt --yes install wine-stable

useradd tpp

mkdir /local
cd /local
mkdir tpp data svn
chown tpp.tpp tpp data svn

cd /local/svn
apt install -y subversion
svn checkout svn://svn.code.sf.net/p/sashimi/code/tags/release_5-1-0

cd /local/svn/release_5-1-0
printf "INSTALL_DIR = /local/tpp\nTPP_BASEURL = /tpp\nTPP_DATADIR = /local/data" > site.mk

make libgd

make all

make install

cpan
      (answer yes)
  make install
  install Bundle::CPAN
      (this takes a long time. At one point you need to hit [ENTER] to accept the 'exit')
  install CGI
  install XML::Parser
  install FindBin::libs
  install JSON
       (you may need to answer 'y' to petulant question)
  quit
