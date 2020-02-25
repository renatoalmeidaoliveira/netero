
irr_prefix -- Generater IRR prefix-list
=======================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This modules runs bgpq3 to generate model based prefix-list



Requirements
------------
The below requirements are needed on the host that executes this module.

- bgpq3



Parameters
----------

  asn32Safe (False, any, False)
    assume that your device is asn32-safe


  IPv (True, any, None)
    IP protocol version


  aggregate (False, any, False)
    If true aggregate the prefix


  asSet (True, any, None)








Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get prefix-list
      irr_prefix:
        asn32_safe: true
        IPv: 4
        as-set: AS1234



Return Values
-------------

  message (success, dict, )
    object containing the IRR prefixes




Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Renato Almeida de Oliveira (renato.a.oliveira@pm.me)

