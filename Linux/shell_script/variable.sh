#!/bin/bash

#user defined varibale
firstvar="hello"
secondvar="friends"

echo "first varible: $firstvar"
echo "second varibale: $secondvar"

#shell defined varibale
echo "current logged in user is $USER"   #USER is predefined varibale

#User input => Read a input prompt from user
read -p "may I know your name?" fullname

echo "Your full name is $fullname"

# arguments
#.variable.sh myname => myname is argument => always file itself is 0th index and 0th arguments

echo "file name is $0"

echo "my name is $1"

echo "executed command : $0 $1"

echo "printing all agument from first index: $@" # '$@' will start getting argument from 1st index

echo "total no of arhguments: $#" # '$#' will print total no of arguments excluding file name


<<run
multiline comment

./filepath/variable.sh firstArg secondArg thirdArg etc.
run
