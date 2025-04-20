#!/bin/bash

<<info
this is an explanation of function.
info

function create_user {
    read -p "enter user: " username

    sudo useradd -m $username

    echo "user created successfully"
}

create_user
# create_user
# create_user

# for ((i=1 ; i<=3; i++))
# do
#     create_user
# done