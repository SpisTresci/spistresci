#!/bin/bash

cd /vagrant

sudo apt-get -y update

# Ommiting prompt while installing mysql
echo "mysql-server-5.5 mysql-server/root_password password root" | debconf-set-selections
echo "mysql-server-5.5 mysql-server/root_password_again password root" | debconf-set-selections

sudo apt-get -y install $(grep -vE "^\s*#" requirements.apt  | tr "\n" " ")

sudo /opt/vagrant_ruby/bin/gem install sass

git clone git://gitslave.git.sourceforge.net/gitroot/gitslave/gitslave /tmp/gitslave
cd /tmp/gitslave/
sudo make install
sudo make install -C contrib
cd -

mkdir /root/.ssh ; touch /root/.ssh/known_hosts ; ssh-keyscan -H "dev.spistresci.pl" >> /root/.ssh/known_hosts ; chmod 600 /root/.ssh/known_hosts
mkdir /home/vagrant/.ssh ; touch /home/vagrant/.ssh/known_hosts ; ssh-keyscan -H "db1.spistresci.pl" >> /home/vagrant/.ssh/known_hosts ; ssh-keyscan -H "solr.spistresci.pl" >> /home/vagrant/.ssh/known_hosts ; chmod 600 /home/vagrant/.ssh/known_hosts

gits fetch
gits populate

find . -name "requirements.pip" -exec sudo pip install -r {} \;

su - vagrant -c "/vagrant/run_tools.sh"
