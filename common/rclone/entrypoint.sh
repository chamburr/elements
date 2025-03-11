#!/bin/sh

rclone --config /etc/rclone/rclone.conf config create minio s3 provider Minio \
  endpoint $S3_ENDPOINT access_key_id $S3_ACCESS_KEY secret_access_key $S3_SECRET_KEY

echo "0 0 * * * /scripts/backup.sh" > /var/spool/cron/crontabs/root

crond -f
