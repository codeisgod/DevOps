#!/bin/bash

echo "========== Creation of User Started ==========="

sudo useradd -m "$1"
echo -e "$2\n$2" | sudo passwd "$1"

echo "========== Creation of User Completed ==========="

<<run
./filepath/create_user_with_arg.sh username password
run