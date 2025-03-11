#!/bin/sh

startup() {
  apk add --no-cache iptables wireguard-tools socat

  printenv CONFIG > /etc/wireguard/wg0.conf

  socat tcp-listen:53,fork,reuseaddr tcp:127.0.0.11:53 &
  p1=$!

  socat -T30 udp-listen:53,fork,reuseaddr udp:127.0.0.11:53 &
  p2=$!

  wg-quick up wg0

  trap shutdown SIGTERM SIGINT SIGQUIT

  wait "$p1" "$p2"
}

shutdown() {
  killall socat

  wg-quick down wg0

  exit 0
}

startup
