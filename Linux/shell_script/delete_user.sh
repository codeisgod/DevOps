#!/bin/bash

echo "========== Deletion of User Started ==========="

sudo userdel -r "$1"    #delete user with directory
#sudo userdel "$1"     #delete user only without directory

echo "========== Deletion of User Completed ==========="

<<run
./filepath/delete_user.sh username
run