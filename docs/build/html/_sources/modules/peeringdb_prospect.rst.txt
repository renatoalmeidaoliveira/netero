
peeringdb_prospect -- Searches for common IXP
=============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This modules uses peeringDB API to lookup for IXP that dst-ASN has in commoon with src-ASN

Providing username and password allows peeringDB to provide restricted information on the query






Parameters
----------

  src-asn (True, any, None)
    The source ASN you whant to lookup for matches on IXP


  dst-asn (True, any, None)
    The destination ASN you whant to lookup for matches on IXP


  username (False, any, None)
    The peeringdb Username


  password (False, any, None)
    The peeringDB password









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get ASN Data
      peeringdb_prospect:
        dst-asn: 15169
        src-asn: 2906



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

