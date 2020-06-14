[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/renatoalmeidaoliveira/netero)
# Ansible Collection - renatoalmeidaoliveira.netero

Netero is a simple utiliy to help network manangement, that aims to encpsulate vendors’ specifics sintax in YAML models based on YANG data model, in this realease it is possible to perfom the following:

* Manage your configuration Backups
* Integrate your backups with Gogs API, with git push and commit
* Consume PeeringDB API for prospection of when some Autonomous System (AS) lies on the same IXP as your AS
* Consume PeeringDB API for gather AS informations as max IPv4/IPv6 prefixes, interfaces address, IRR-ASSET
* Encapsulate BGPq3/BGPq4 for generation of prefix-list of a given IRR-ASSET

# Requirements

* [git](https://git-scm.com/)
* [bgpq3](https://github.com/snar/bgpq3) or [bgpq4](https://github.com/bgp/bgpq4)
* [requests](https://pypi.org/project/requests/)
* [netmiko](https://pypi.org/project/netmiko/)
* [ncclient](https://pypi.org/project/ncclient/)

# Installing

[Ansible Galaxy](https://galaxy.ansible.com/) is the default source of Ansible collections for the ansible-galaxy tool. We can install Netero Ansible collection by running: 

``   $ ansible-galaxy collection install renatoalmeidaoliveira.netero `` 

# Use Cases 

Netero is built for a multivendor environment, where all the  vendors specifics sintax are encapsulated in roles that deliver an uniform interface for the tasks.
For acomodate the specifc syntax of the vendors Netero relies on the Roles abstraction and on data models based on OpenConfig or YANG, as described in Figure 1.
![Figure 1. Multi Vendor conception](https://github.com/renatoalmeidaoliveira/netero/blob/assets/design.png) <p align="center">
  *Figure 1. Multi Vendor conception*
</p>

## Configuration Backup

For the configuration Backup Netero encapsulate the modules, ios_facts, fortios_config, iosxr_facts, routeros_facts for configuration gathering, and the module lineinfile for sanitize the configuration file removing password lines and collection timestamp.
A recommended use follow the Figure 2, that crates a fresh repository on Gogs SVN, clone the repository, gather and sanitize the configuration and then commit and push the configurations.

![Figure 2. Backup Process](https://github.com/renatoalmeidaoliveira/netero/blob/assets/backup.png) <p align="center">
  *Figure 2. Backup Process*
</p>

```
- name: Setup repositories
  collections:
    - renatoalmeidaoliveira.netero

  hosts:  all

  tasks:

   - name: Create Repository
     gogs_createrepo:
        gogsURL: "http://gogs.local:3000/"
        organization: "netero"
        name: "{{ inventory_hostname }}"
        accessToken: "0bba381ce3df8208591e067a4abae72a556974ce"
     delegate_to: localhost
   
   - name: Clone Repository
     git:
        repo: "git@gogs.local:netero/{{ inventory_hostname }}.git"
        dest: "{{ inventory_hostname }}"
     delegate_to: localhost

   - name: Incluir Roles
     include_role:
       name: "{{ ansible_network_os }}"
     vars:
       - netero_mode: "backup"

   - name: Commit
     git_commit:
       path: "{{ inventory_hostname }}"
     delegate_to: localhost

```

## BGP Routing Policy configuration

For routing policy configuration Netero relies on BGPq3/BGPq4 for gathering the IRR AS-SET object and deliver an JSON object with the desired prefixes.
For the AS-SET the peeringdb_getasn module uses the PeeringDB API and extracts relevant routing policy information’s like MAX_PREFIX, AS-SET and IP Address of IXP interfaces.
With the information’s above it is possible by following the process of Figure 3, create an automated configuration for BGP network policies.

![Figure 3. BGP Configuration Process](https://github.com/renatoalmeidaoliveira/netero/blob/assets/generateFilters.png) <p align="center">
  *Figure 2. BGP Configuration Process*
</p>

```
- name: BGP Routing configuration
  collections:
    - renatoalmeidaoliveira.netero

  hosts: all

  tasks:

    - name: Get ASN Data
      peeringdb_getasn:
        asn: 204092
        ix-id: 1670
      register: ASNData

    - name: print ASNData
      debug:
        var: ASNData

    - name: Get IRR Prefix
      irr_prefix:
        asn32Safe: True
        IPv: 4
        asSet: "{{ item }}"
        aggregate: true
      with_items:
        - "{{ ASNData.message.irr_as_set }}"
      register: IRRData

    - name: Make Configuration File
      template:
        src: Parse.j2
        dest: Config
        mode: 0777
      delegate_to: localhost

    - name: Apply Config
      ios_config:
        src: Config
      delegate_to: localhost      

```
# Next Steps

The configuration module, that will read model files and configure the network devices

# Documentation Link:

http://netero.renatooliveira.eng.br/