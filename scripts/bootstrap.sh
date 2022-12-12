#!/bin/sh

prepare() {
  if [ -z "$1" ]; then
    echo 'Usage: ./scripts/bootstrap.sh name'
    exit 1
  fi

  ansible-galaxy collection install -r ansible/requirements.yml > /dev/null
}

install() {
  echo 'Installing...'

  ./scripts/ansible.sh playbook ansible/main.yml --tags common --limit "$1"

  sed -i \
    -e "s/^USER=.*/USER=$(cat ansible/group_vars/all.yml | yq '.username')/" \
    -e "s/^PASSWORD=.*/PASSWORD=/" \
    .env

  export NETMAKER_TOKEN=$(grep NETMAKER_TOKEN= .env | cut -d '=' -f2-)

  ./scripts/ansible.sh playbook ansible/main.yml --skip-tags common --limit "$1"
}

prepare "$@"
install "$@"
