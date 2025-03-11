#!/bin/bash

prepare() {
  export SOPS_AGE_KEY="$SOPS_KEY"
  export SOPS_AGE_RECIPIENTS="$SOPS_RECIPIENTS"

  find . -mindepth 2 -name .sops.env -printf '%h\n' \
    | xargs -I{} sh -c 'sops -d --output-type binary --output {}/.env {}/.sops.env'
}

run() {
  echo 'Running...'

  hostname=$(hostname)

  docker compose ls -q --all \
    | xargs -I{} sh -c 'if [ -z "$(find common '$hostname' -type d -name {})" ]; then echo {}; fi' \
    | xargs -I{} sh -c 'docker compose -p {} down --remove-orphans --volumes'

  find common -name docker-compose.yml \
    | xargs -I{} sh -c 'cd "$(dirname {})" && docker compose up --remove-orphans -d'

  find $hostname -name docker-compose.yml \
    | xargs -I{} sh -c 'cd "$(dirname {})" && docker compose up --remove-orphans -d'

  docker image prune --all --force
}

(
  flock 200
  prepare
  run
) 200>/var/lock/docker-compose.lock
