#!/bin/sh

(
  sleep 15
  ip route add 10.0.0.0/24 dev tailscale0 || true
) &

exec /usr/local/bin/containerboot
