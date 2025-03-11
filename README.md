# Elements

My external infrastructure and Docker applications written as code.

This project utilises Infrastructure as Code and GitOps to automate the provisioning, operating and
updating of applications in my various cloud servers. Furthermore, this repository can also serve as
a good framework for you to build your own infrastructure.

Feel free to open a [GitHub issue](https://github.com/chamburr/elements/issues) if you have any
questions!

## Installation

First, get a server running Ubuntu, which could be rented from any cloud provider. Then, install the
prerequisites in Brewfile and update Ansible and environmental variables. Finally, run
`./scripts/bootstrap.sh name` to install everything on the server! You can repeat this process to
configure multiple servers.

## Core components

<table>
  <tr>
    <th>Logo</th>
    <th>Name</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img width="32" src="https://avatars.githubusercontent.com/u/1507452?s=200&v=4"></td>
    <td><a href="https://ansible.com">Ansible</a></td>
    <td>Bare metal provisioning and configuration</td>
  </tr>
  <tr>
    <td><img width="32" src="https://avatars.githubusercontent.com/u/5429470?s=200&v=4"></td>
    <td><a href="https://docker.com">Docker</a></td>
    <td>Orchestration system for managing containers</td>
  </tr>
  <tr>
    <td><img width="32" src="https://icon.icepanel.io/Technology/svg/Traefik-Proxy.svg"></td>
    <td><a href="https://traefik.io">Traefik</a></td>
    <td>Cloud native ingress controller for Docker</td>
  </tr>
  <tr>
    <td><img width="32" src="https://avatars.githubusercontent.com/u/4604537?s=200&v=4"></td>
    <td><a href="https://ubuntu.com">Ubuntu</a></td>
    <td>Main Linux distribution for infrastructure</td>
  </tr>
  <tr>
    <td><img width="32" src="https://avatars.githubusercontent.com/u/129185620?s=200&v=4"></td>
    <td><a href="https://github.com/getsops/sops">SOPS</a></td>
    <td>Secrets and encryption management system</td>
  </tr>
  <tr>
    <td><img width="32" src="https://avatars.githubusercontent.com/u/84780935?s=200&v=4"></td>
    <td><a href="https://woodpecker-ci.org">Woodpecker</a></td>
    <td>Continuous integration and delivery platform</td>
  </tr>
</table>

## Hardware

My infrastructure currently consists of multiple nodes with the following specifications.

- Radon: 8 vCPU, 12GB RAM, 100GB SSD (Los Angeles)
- Xenon: 1 vCPU, 1GB RAM, 25GB SSD (Singapore)
- Krypton: 2 vCPU, 2GB RAM, 60GB SSD (Chicago)

## License

This project is licensed under the [MIT License](LICENSE).
