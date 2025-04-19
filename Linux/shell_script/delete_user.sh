#!/bin/bash

echo "========== Deletion of User Started ==========="

sudo userdel -r "$1"    #delete user with directory
#sudo userdel "$1"     #delete user only without directory

cat /etc/passwd | grep "$1" | wc    # /etc/passwd is listed all users
# /etc/passwd is listed all users -> grep (filter only username)
#checking wc -> word count to make sure it have 0 values

#cat /etc/passwd | grep "$1" | wc | awk '{print $1}'

echo "as wordcount is 0, user deleted successfully."

echo "========== Deletion of User Completed ==========="

<<run
./filepath/delete_user.sh username
run