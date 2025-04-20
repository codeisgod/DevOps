#!/bin/bash

<<syntax
for ((initial; condition; inc/dec))
do
    for_body
done
syntax

for ((num=1 ; num<=10; num++))
do
    echo "$num"
    echo "hello"
done