#!/bin/bash

export ENV=dev
screen -dmS runserver /vagrant/manage.py runserver 0.0.0.0:8000
screen -dmS solr ssh tunel@solr1.spistresci.pl -p 1337 -L 10000:localhost:8090
screen -dmS mysql ssh root@db1.spistresci.pl -p 1337 -L 6603:localhost:3306
screen -dmS sass sass --watch /vagrant/spistresci/static/scss:/vagrant/spistresci/static/css/

