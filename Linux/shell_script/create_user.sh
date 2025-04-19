#!/bin/bash

<<help
multiline comment start with
<<anyword

anyword
also end with same name
help

#======================================================

echo "========== Creation of User Started ==========="

#read username and password for user creation
read -p "enter the username:" username
read -p "enter the password:" password

#create user by linux command => useradd -m username => -m to create folder for user
sudo useradd -m "$username"

#attaching password with -e (enable backslash or escape like \n) => put password two times for new password and confirm password.
echo -e "$password\n$password" | sudo passwd "$username"

echo "========== Creation of User Completed ==========="


<<run
./filepath create_user.sh
run
