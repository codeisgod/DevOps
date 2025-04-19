#!/bin/bash

echo "========== Deletion of User Started ==========="

sudo userdel -r "$1"    #delete user with directory
#sudo userdel "$1"     #delete user only without directory

cat /etc/passwd | grep "$1" | wc    # /etc/passwd is listed all users

echo "as wordcount is 0, user deleted successfully."

echo "========== Deletion of User Completed ==========="

<<run
./filepath/delete_user.sh username
run