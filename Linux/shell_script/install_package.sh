#!/bin/bash

<<info
this script will install the packages that you pass in the arguments

eg.
./install_package.sh nginx
./install_package.sh docker.io
./install_package.sh unzip
info

echo "Installing $1"

sudo yum -y update > /dev/null     # /dev/null will not write anything on console (saved to this which ios null)
sudo yum install $1 -y

echo "Installation Completed."


<<run
./filepath/install_package.sh packege_name
run