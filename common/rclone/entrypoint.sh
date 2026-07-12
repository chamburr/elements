#!/bin/sh

apk add --no-cache curl

mkdir -p /etc/rclone

echo "$NTFY_TOKEN" > /etc/rclone/ntfy_token

rclone --config /etc/rclone/rclone.conf config create rustfs s3 provider Minio \
  endpoint $S3_ENDPOINT access_key_id $S3_ACCESS_KEY secret_access_key $S3_SECRET_KEY

echo "0 0 * * * /scripts/backup.sh" > /var/spool/cron/crontabs/root

exec crond -f
