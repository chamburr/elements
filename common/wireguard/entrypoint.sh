#!/bin/sh

startup() {
  apk add --no-cache iptables wireguard-tools
  apk add --no-cache --repository=http://dl-cdn.alpinelinux.org/alpine/v3.18/main socat=1.7.4.4-r1

  printenv CONFIG > /etc/wireguard/wg0.conf

  socat udp-recvfrom:53,fork udp-sendto:127.0.0.11:53 &
  p1=$!

  socat tcp-listen:53,reuseaddr,fork tcp:127.0.0.11:53 &
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
