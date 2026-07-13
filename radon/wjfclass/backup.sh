#!/bin/sh

apk add --no-cache mariadb-client

echo '0 23 * * * mariadb-dump -h mariadb -u root --single-transaction --skip-ssl wiki > /backup/data.sql' > /var/spool/cron/crontabs/root

exec crond -f
