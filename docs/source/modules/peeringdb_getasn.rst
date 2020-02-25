
peeringdb_getasn -- Searches for an ASN policy and interfaces
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This modules encapsules peeringDB API to search for an specific ASN his interfaces and policy indormations






Parameters
----------

  asn (True, any, None)
    The searched ASN


  username (False, any, None)
    Your peeringDB User


  password (False, any, None)
    Your peeringDB password


  ix-id (False, any, None)
    The peeringDB IXP ID


  ix-name (False, any, None)
    The peerigDB IXP Name









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Search ASN 15169
      peeringdb_getasn:
        asn: 15169
        ix-id: 171



Return Values
-------------

  object (success, dict, )
    object representing ASN data




Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Renato Almeida de Oliveira (renato.a.oliveira@pm.me)

