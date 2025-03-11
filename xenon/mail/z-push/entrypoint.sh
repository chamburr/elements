#!/bin/sh

CALDAV_CONFIG_FILE="./backend/caldav/config.php"
sed -i \
  -e "s|('CALDAV_SERVER', 'caldavserver.domain.com')|('CALDAV_SERVER', ${IMAP_SERVER})|" \
  -e "s|('CALDAV_PATH', '/caldav.php/%u/')|('CALDAV_PATH', '${CALDAV_PATH}')|" \
  -e "s|('CALDAV_SUPPORTS_SYNC', false)|('CALDAV_SUPPORTS_SYNC', true)|" \
  "$CALDAV_CONFIG_FILE"

CARDDAV_CONFIG_FILE="./backend/carddav/config.php"
sed -i \
  -e "s|('CARDDAV_SERVER', 'localhost')|('CARDDAV_SERVER', ${IMAP_SERVER})|" \
  -e "s|('CARDDAV_PATH', '/caldav.php/%u/')|('CARDDAV_PATH', '${CALDAV_PATH}')|" \
  -e "s|('CARDDAV_DEFAULT_PATH', '/caldav.php/%u/addresses/')|('CARDDAV_DEFAULT_PATH', '${CALDAV_PATH}contacts/')|" \
  -e "s|('CARDDAV_GAL_PATH', '/caldav.php/%d/GAL/')|('CARDDAV_GAL_PATH', '')|" \
  -e "s|('CARDDAV_SUPPORTS_SYNC', false)|('CARDDAV_SUPPORTS_SYNC', true)|" \
  "$CARDDAV_CONFIG_FILE"

/usr/local/bin/preflight.sh
