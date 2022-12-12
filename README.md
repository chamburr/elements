# Elements

My external infrastructure and Docker applications written as code.

This project utilises Infrastructure as Code and GitOps to automate the provisioning, operating and
updating of applications in my various cloud servers. Furthermore, this repository can also serve as
a good framework for you to build your own infrastructure.

Feel free to open a [GitHub issue](https://github.com/chamburr/elements/issues) if you have any
questions!

## Installation

First, get a server running the latest Ubuntu LTS software, which could be rented from any cloud
provider. Then, install prerequisites in Brewfile and update Ansible and environmental variables.
Finally, run `./scripts/bootstrap.sh name` to install everything on the server! You can repeat this
process to configure multiple servers.

## Core components

<table>
  <tr>
    <th>Logo</th>
    <th>Name</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img width="32" src="https://vectorlogo.zone/logos/ansible/ansible-icon.svg"></td>
    <td><a href="https://ansible.com">Ansible</a></td>
    <td>Bare metal provisioning and configuration</td>
  </tr>
  <tr>
    <td><img width="32" src="https://www.vectorlogo.zone/logos/docker/docker-icon.svg"></td>
    <td><a href="https://docker.com">Docker</a></td>
    <td>Orchestration system for managing containers</td>
  </tr>
  <tr>
    <td><img width="32" src="https://www.vectorlogo.zone/logos/droneio/droneio-icon.svg"></td>
    <td><a href="https://drone.io">Drone</a></td>
    <td>Continuous integration and delivery platform</td>
  </tr>
  <tr>
    <td><img width="32" src="https://vectorlogo.zone/logos/traefikio/traefikio-icon.svg"></td>
    <td><a href="https://traefik.io">Traefik</a></td>
    <td>Cloud native ingress controller for Docker</td>
  </tr>
  <tr>
    <td><img width="32" src="https://www.vectorlogo.zone/logos/ubuntu/ubuntu-icon.svg"></td>
    <td><a href="https://ubuntu.com">Ubuntu</a></td>
    <td>Main operating system for infrastructure</td>
  </tr>
  <tr>
    <td><img width="32" src="https://www.vectorlogo.zone/logos/mozilla/mozilla-icon.svg"></td>
    <td><a href="https://github.com/mozilla/sops">SOPS</a></td>
    <td>Secrets and encryption management system</td>
  </tr>
</table>

## Hardware

My infrastructure currently consists of multiple nodes with the following specifications.

- Radon: 8 vCPU, 16GB RAM, 100GB SSD (Los Angeles)
- Xenon: 1 vCPU, 1GB RAM, 25GB SSD (Singapore)

## License

This project is licensed under the [MIT License](LICENSE).
