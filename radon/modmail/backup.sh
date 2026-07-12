#!/bin/sh

apk add --no-cache postgresql17-client

echo '0 23 * * * pg_dump -h postgres -U postgres -d modmail > /backup/data.sql' > /var/spool/cron/crontabs/root

exec crond -f
