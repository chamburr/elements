#!/bin/sh

retention=7

hostname=$(cat /scripts/hostname)
date=$(date +%F)

files=$(find /scripts/data -type f -mtime +$(($retention - 1)) | sed 's/.*\///')

echo $files | xargs -I{} rclone --config /etc/rclone/rclone.conf purge minio:elements/_old/$hostname/{}
echo $files | xargs -I{} rm /scripts/data/{}

rclone --config /etc/rclone/rclone.conf sync /data minio:elements/$hostname \
  --s3-no-check-bucket --backup-dir minio:elements/_old/$hostname/$date \
  --exclude /backingFsBlockDev --exclude "/{{[0-9a-f]{64}}}"

touch "/scripts/data/$date"
