#!/bin/bash

<<info
this shell script checks if user exits.
info

read -p "Enter the username you wish to check" username

count=$(cat /etc/passwd | grep $username | wc | awk '{print $1}')

if [ $count -eq 0 ];
then
        echo "user does not exits"
else
        echo "user exits"
fi         #end of if

<<run
./filepath/check_if_user_exits.sh
run



<<syntax
if [ condition ]; then
    if body
else
    else body
fi
syntax