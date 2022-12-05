#!/bin/sh

prepare() {
  export SOPS_AGE_KEY=$(grep AGE_KEY= .env | cut -d '=' -f2-)
  export SOPS_AGE_RECIPIENTS=$(grep AGE_RECIPIENTS= .env | cut -d '=' -f2-)
}

encrypt() {
  echo "Encrypting..."

  find . -mindepth 2 -name .env \
    | xargs -I{} sh -c 'sops -e --input-type binary --output "$(echo {} | sed s/env/sops.env/)" {}'
}

decrypt() {
  echo "Decrypting..."

  find . -mindepth 2 -name .sops.env \
    | xargs -I{} sh -c 'sops -d --output-type binary --output "$(echo {} | sed s/sops.env/env/)" {}'
}

prepare

if [ "$1" = '' ]; then
  encrypt
elif [ "$1" = '--decrypt' ]; then
  decrypt
fi
