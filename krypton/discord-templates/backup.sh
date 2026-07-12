#!/bin/sh

apk add --no-cache sqlite

echo '0 23 * * * sqlite3 /data/data.db ".backup /backup/data.db"' > /var/spool/cron/crontabs/root

exec crond -f
