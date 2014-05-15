#!/bin/bash

cd /vagrant

sudo apt-get -y update

# Ommiting "apt-get install mysql" prompt
#echo "mysql-server-5.5 mysql-server/root_password password root" | debconf-set-selections
#echo "mysql-server-5.5 mysql-server/root_password_again password root" | debconf-set-selections

sudo apt-get -y install $(grep -vE "^\s*#" requirements.apt  | tr "\n" " ")

git clone git://gitslave.git.sourceforge.net/gitroot/gitslave/gitslave /tmp/gitslave
cd /tmp/gitslave/
sudo make install
sudo make install -C contrib
cd -

gits fetch
gits populate

find . -name "requirements.pip" -exec sudo pip install -r {} \;

