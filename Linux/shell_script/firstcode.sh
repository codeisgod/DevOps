#!/bin/bash
<<help
multiline comment

run script => ./filepath/filename.sh
help

# ================== script started here ==================

echo "Hello Friends"

echo "SHELL path: $SHELL" #SHELL is system variable

#Creating Directory
#mkdir testing    #this will create testing directory once only. from 2nd onward it provide error
mkdir -p testing  #this command will create directory for first and if directory is already there thne ignore it.

cd testing

touch test.txt

echo "this is test file" > test.txt