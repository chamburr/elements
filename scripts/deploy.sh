#!/bin/sh

prepare() {
  find . -mindepth 2 -name .sops.env -printf '%h\n' \
    | xargs -I{} sh -c 'sops -d --output-type binary --output {}/.env {}/.sops.env'
}

run() {
  echo 'Running...'

  hostname=$(hostname)

  find common $hostname -name docker-compose.yml
    | xargs -I{} sh -c 'cd "$(dirname {})" && docker compose up --remove-orphans -d'

  docker compose ls -q --all
    | xargs -I{} sh -c 'if [ -z "$(find common '$hostname' -type d -name {})" ]; then echo {}; fi'
    | xargs -I{} sh -c 'docker compose -p {} down --remove-orphans --volumes'

  docker image prune --all --force
}

prepare
run
