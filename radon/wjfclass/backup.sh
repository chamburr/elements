#!/bin/sh

apk add --no-cache mariadb-client

echo '0 23 * * * mysqldump -h mariadb -u root --single-transaction wiki > /backup/data.sql' > /var/spool/cron/crontabs/root

exec crond -f
