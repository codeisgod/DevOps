#!/bin/bash

<<info
this shell script will take periodic backups
info

src=$1
dest=$2

timestamp=$(date '+%Y-%m-%d-%H-%M-%S')   #date in YYYY-MM-DD-Hour-Minut-Second

# zip "$dest/backup-$timestamp.zip" $src
zip "$dest/backup-$timestamp.zip" $src > /dev/null

echo "backup completed"

# aws s3 sync $dest s3://bucket-name
# echo "backup completed and uploaded to s3"

<<run
./filepath/backup.sh <source> <destination>
run

<<cron
-> use crontab guru
-> total five parts are there
    -> min hour day(month) month day(week)
    -> * means all

crontab -e    => to open crontab
choose editor => 2
*/2 * * * *     => every 2 min
*/2 * * * * sh /home/path/backuo.sh /home/cloud_user/scripts /home/cloud_user/backup
or
*/2 * * * * bash /home/path/backuo.sh /home/cloud_user/scripts /home/cloud_user/backup

watch ls --> to watch live logs of command ls
cron

<<create_backup_on_s3
go to AWS
go to S3
create new bucket
provide bucket name

go to IAM 
create user backup_user and provide permission of S3 all

Install AWS CLI on Linux
-> curl, upzip, install
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

configure AWS
-> aws configure
-> required access key id
    -> go to created user in IAM 
    -> IAM -> Users -> backup_user
    -> go to security credentials
    -> see access keys
    -> create access key
    -> select usecase 
    -> access key and secreat access key created
-> put access key ID 
-> put Secreat Access key
-> leave Default region name and output format

check configured or not
-> aws s3 ls   ==> list all bucket

store backup in s3
-> aws s3 sync <localpath> <s3URI>
-> aws s3 sync <localpath> s3://<bucket-name>
create_backup_on_s3