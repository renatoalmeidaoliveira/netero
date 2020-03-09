.. Netero documentation master file, created by
   sphinx-quickstart on Sun Feb 23 22:32:35 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. meta::
   :google-site-verification: SnqqZA5-pfEcJ-qbLboUbUwXV5GuaS1aguyNSHcWvQA
   :description lang=en:
        Netero is an Ansible collection that encapsulates PeeringDB API and BGPq3/BGPq4 for automatic generation of BGP routing policies.

Welcome to Netero's documentation!
==================================

 Netero is a simple utiliy to help network manangement, that aims to encpsulate vendors' specifics sintax in YAML models based on YANG data model, in this realease it is possible to perfom the following:

* Manage your configuration Backups
* Integrate your backups with Gogs API, with git push and commit
* Consume PeeringDB API for prospection of when some Autonomous System (AS) lies on the same IXP as your AS
* Consume PeeringDB API for gather AS informations as max IPv4/IPv6 prefixes, interfaces address, IRR-ASSET
* Encapsulate BGPq3 or BGPq4 for generation of prefix-list of a given IRR-ASSET

Quick Start
==================================

Clone our `sample repository <https://github.com/renatoalmeidaoliveira/netero-sample.git>`_ , where you’re going to find some playbooks samples, and a Jinja2 template for RouterOS policy configurations.

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src=" https://www.youtube.com/embed/41vViNm1yu4" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>



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
