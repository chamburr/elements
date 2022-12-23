#!/bin/sh

prepare() {
  export SOPS_AGE_KEY=$(grep ^AGE_KEY= .env | cut -d '=' -f2-)
  export SOPS_AGE_RECIPIENTS=$(grep ^AGE_RECIPIENTS= .env | cut -d '=' -f2-)
}

encrypt() {
  echo 'Encrypting...'

  find . -mindepth 2 -name .env -printf '%h\n' \
    | xargs -I{} sh -c 'if [ ! -f "{}/.sops.env" ] ||
    [ "$(sops -d --output-type binary {}/.sops.env)" != "$(cat {}/.env)" ]; then
    sops -e --input-type binary --output {}/.sops.env {}/.env; fi'
}

prepare
encrypt
