#!/bin/bash

sudo apt-get install $(grep -vE "^\s*#" requirements.apt  | tr "\n" " ")

git clone git://gitslave.git.sourceforge.net/gitroot/gitslave/gitslave /tmp/gitslave
cd /tmp/gitslave/
sudo make install
sudo make install -C contrib
cd -

gits fetch
gits populate

find . -name "requirements.pip" -exec pip install -r {} \;

