#!/bin/sh

apk add --no-cache mariadb-client

echo '0 23 * * * mysqldump -h mysql -u root --single-transaction ghost > /backup/data.sql' > /var/spool/cron/crontabs/root

exec crond -f
