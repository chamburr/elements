#!/bin/sh

hostname=$(cat /scripts/hostname)
date=$(date +%F)

for marker in $(find /scripts/data -type f -mtime +6); do
  old_date=$(basename "$marker")
  output=$(rclone --config /etc/rclone/rclone.conf purge rustfs:elements/_old/$hostname/$old_date 2>&1)
  status=$?
  if [ $status -eq 0 ] || echo "$output" | grep -qi "directory not found"; then
    rm "$marker"
  fi
done

rclone --config /etc/rclone/rclone.conf sync /data rustfs:elements/$hostname \
  --s3-no-check-bucket --backup-dir rustfs:elements/_old/$hostname/$date \
  --exclude /backingFsBlockDev --exclude "/{{[0-9a-f]{64}}}/**" \
  --exclude /blog_mysql/** --exclude /areticle_mysql/** \
  --exclude /wjfclass_mariadb/** --exclude /modmail_postgres/** \
  --exclude /discord-tags_tags/_data/data.db \
  --exclude /discord-templates_templates/_data/data.db

if [ $? -ne 0 ]; then
  curl -s \
    -H "Authorization: Bearer $(cat /etc/rclone/ntfy_token)" \
    -H "Title: Elements backup failed." \
    -d "The nightly backup on $hostname failed. Check the rclone container logs." \
    https://ntfy.chamburr.xyz/miscellaneous
fi

touch "/scripts/data/$date"
