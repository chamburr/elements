#!/bin/sh

startup() {
  apk add --no-cache socat wireguard-tools

  printenv CONFIG > /etc/wireguard/wg0.conf

  socat udp-listen:53,reuseaddr,fork udp:10.0.0.1:53 &
  p1=$!

  socat tcp-listen:53,reuseaddr,fork tcp:10.0.0.1:53 &
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
