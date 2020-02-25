.. Netero documentation master file, created by
   sphinx-quickstart on Sun Feb 23 22:32:35 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Netero's documentation!
==================================

 Netero is a simple utiliy to help network manangement, that aims to encpsulate vendors' specifics sintax in YAML models based on YANG data model, in this realease it is possible to perfom the following:

* Manage your configuration Backups
* Integrate your backups with Gogs API, with git push and commit
* Consume PeeringDB API for prospection of when some Autonomous System (AS) lies on the same IXP as your AS
* Consume PeeringDB API for gather AS informations as max IPv4/IPv6 prefixes, interfaces address, IRR-ASSET
* Encapsulate BGPQ3 for generation of prefix-list of a given IRR-ASSET

Next Steps 
===================================

* The configuration module, that will read model files and configure the network devices

.. toctree::
   :maxdepth: 2
   :caption: Using Netero Collection
   
   install
   examples

.. toctree::
   :maxdepth: 1
   :caption: References

   modules
