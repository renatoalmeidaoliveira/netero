Use Cases
=============

Configuration Backup
-----------------------------

For the configuration backup you can use the backup mode and netero roles or use the modules directly.

Using the roles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The netero roles encapsulate the configuration gathering of the devices, and for utilization you must setup the netero mode to backup, and separate your devices in groups of vendors, i.e., IOS, IOS-XR, ROUTEROS, etc.

So for configuration management your playbook must perform the following tasks:

1.      Create the repository in your favorite repository manager, in the example the gogs_createrepo are going to be used.
2.      Clone the previously created repositories.

.. code-block:: yaml+jinja

    - name: Setup repositories
      collections:
        - renatoalmeidaoliveira.netero

      hosts: all

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


3.      Create a play for each of your device vendors and set the respective group.

.. code-block:: yaml+jinja

    - name: Collect IOS-XR configuration
      collections:
        - renatoalmeidaoliveira.netero
      vars:
        - netero_mode: "backup"
      hosts: iosxr
      roles:
        - iosxr
    - name: Collect MK configuration
      collections:
        - renatoalmeidaoliveira.netero
      vars:
        - netero_mode: "backup"
      hosts: routeros
      roles:
        - routeros

.. warning::
  
   Remember to configure the netero_mode variable to "backup"
   Suported Vendors:
   * IOS
   * IOS-XR
   * MikroTik
   * Fortgate


4.      Commit and push the repositories .

.. code-block:: yaml+jinja

    - name: Commit and push reporitories

      collections:
        - renatoalmeidaoliveira.netero

      hosts: all

      tasks:

      - name: Commit
        git_commit:
          path: "{{ inventory_hostname }}"
        delegate_to: localhost
      - name: Push
        git_push:
          path: "{{ inventory_hostname }}"
        delegate_to: localhost

Using the modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For make your backup with the modules you could use the following steps

1. Create the repository on Gogs, if the repository already exists the module runs without changes

.. code-block:: yaml+jinja

   - name: Create Repository
     gogs_createrepo:
        gogsURL: "<Gogs URL>"
        organization: "acme"
        name: "{{ inventory_hostname }}"
        accessToken: <accessToken>
      delegate_to: localhost

2. Clone the configuration repository

.. code-block:: yaml+jinja

    - name: Clone Repository
      git:
        repo: "<Gogs URL>:<org|user>/{{ inventory_hostname }}.git"
        dest: "{{ inventory_hostname }}"
      delegate_to: localhost

.. tip::

   Setup the SSH Keys with Gogs and the Server runnig Ansible, instead of using username and password

3. Extract your device configuration using any module you want.

.. code-block:: yaml+jinja

   - name: Gather device configuration
     routeros_facts:
       gather_subset:
         - config

4. Create the configuration File

.. code-block:: yaml+jinja

    - name: Create configuration File
      copy:
        content: "{{ansible_net_config}}"
        dest: "{{ inventory_hostname }}/{{ inventory_hostname }}.cfg"
      delegate_to: localhost

5. Sanitize your configuration file

In this step remove any line containing passwords, and the timestamp of the collect, ie usually the first line

.. code-block:: yaml+jinja

    - name: Sanitize Configuration File
      lineinfile:
        path: "{{ inventory_hostname }}/{{ inventory_hostname }}.cfg"
        state: absent
        regexp: '# \w+/\d+/\d+ \d+:\d+:\d+.*'
      delegate_to: localhost

6. Commit the local repository


.. important::

   Make sure that the user runnig the ansible-playbook have the git user.name and user.email configured

.. code-block:: yaml+jinja
   
   - name: Commit
     git_commit:
        path: "{{ inventory_hostname }}"
     delegate_to: localhost

7. Push the repository

.. code-block:: yaml+jinja

    - name: Push
      git_push:
        path: "{{ inventory_hostname }}"
      delegate_to: localhost

Creating routing policies
-----------------------------

Using the modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For creating routing policies we gonna use the peergindb_getasn and irr_prefix modules, for extract all the ASN informations and then using Jinja2 templates it is possible to create the desired configuration

1. Consultando a API do PeeringDB para extrair as informações do ASN:

.. code-block:: yaml+jinja

    - name: Get ASN Data
      peeringdb_getasn:
        asn: 204092
        ix-id: 1670
      register: ASNData

**SAMPLE OUTPUT**

.. code-block:: 

    "ASNData.message": {
      "ASN": 204092,
      "info_ipv6": true,
      "info_prefixes4": 20,
      "info_prefixes6": 20,
      "info_unicast": true,
      "interfaces": [
          {
              "ipaddr4": "185.1.89.10",
              "ipaddr6": "2001:7f8:b1::a",
              "speed": 1000
          }
      ],
      "irr_as_set": [
          "AS-GRIFON"
      ],
      "poc_set": []
  }

2. Using the ASN Data as input for irr_prefix:

.. code-block:: yaml+jinja

  - name: Get IRR Prefix
    irr_prefix:
      asn32Safe: True
      IPv: 4
      asSet: "{{ item }} "
      aggregate: true
    with_items:
      - "{{ ASNData.message.irr_as_set }}"
    register: IRRData


**SAMPLE OUTPUT**

.. code-block::

    "IRRData.results": [
            {
                "ansible_loop_var": "item",
                "changed": true,
                "failed": false,
                "invocation": {
                    "module_args": {
                        "IPv": "4",
                        "aggregate": true,
                        "asSet": "AS-GRIFON ",
                        "asn32Safe": true
                    }
                },
                "item": "AS-GRIFON",
                "message": {
                    "irr_prefix": [
                        {
                            "exact": true,
                            "prefix": "23.128.24.0/24"
                        },
                        {
                            "exact": true,
                            "prefix": "23.128.25.0/25"
                        },
                        {
                            "exact": true,
                            "prefix": "23.128.25.240/28"
                        }
                    ]
                }
            }
        ]
    }

                
3. Create a Jinja2 template for create your device configuration
4. Apply the configuration to your device

Prospect ASN
-----------------------------

Using the modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module was created to simplify ASN information gathering, imagine the following scenario:

* Your NetFlow monitoring system shows you that 30% of your traffic goes to some ASN, and to optimize your traffic you want to make an peering agreement with that ASN but you don’t know any contact number and if that ASN is on the same IXP with your.
* After getting that information you want to send the Policy contact an email asking for the peering agreement

That can be configured as follow:

1. Configure the module with your ASN in src-asn and the desired ASNs in dst-asn, and with your peeringDB username and password:

.. code-block:: yaml+jinja

  - name: Prospect ASN Data
    peeringdb_prospect:
      src-asn: 1916
      dst-asn: 1251
      username : Joe
      password: secret


**SAMPLE OUTPUT** 

.. code-block::

    "prospectData": {
        "changed": false,
        "failed": false,
        "message": [
            {
                "1251": {
                    "IXs": [
                        {
                            "id": 171,
                            "name": "IX.br (PTT.br) São Paulo: ATM/MPLA"
                        },
                        {
                            "id": 119,
                            "name": "Equinix São Paulo: Equinix IX - SP Metro"
                        }
                    ],
                    "name": "ANSP",
                    "poc_set": [
                        {
                            "created": "*************",
                            "email": "*****@*****",
                            "id": *******,
                            "name": "********",
                            "phone": "**********",
                            "role": "Technical",
                            "status": "ok",
                            "updated": "************",
                            "url": "*******",
                            "visible": "Users"
                        }
                    ]
                }
            }
        ]
    }

.. warning::

   Contact data sanitized.


2. Create a template with Jinja using ASN data
3. Send an email asking for your peering session
