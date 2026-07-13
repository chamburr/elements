#!/bin/sh

apk add --no-cache mariadb-client mariadb-connector-c

echo '0 23 * * * mariadb-dump -h mysql -u root --single-transaction --skip-ssl ghost > /backup/data.sql' > /var/spool/cron/crontabs/root

exec crond -f
