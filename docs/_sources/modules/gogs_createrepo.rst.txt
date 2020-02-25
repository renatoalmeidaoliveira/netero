
gogs_createrepo -- Create a repository on Gogs
==============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module encapusles Gogs API to create a repository






Parameters
----------

  gogsURL (True, any, None)
    The Gogs Server URL


  user (False, any, None)
    The user that owns the repository, This argument is mutually exclusive with organization.


  organization (False, any, None)
    The organization that owns the repository, This argument is mutually exclusive with user.


  name (True, any, None)
    The repository name


  description (False, any, None)
    A short description of the repository


  private (False, any, False)
    Either true to create a private repository, or false to create a public one


  autoInit (False, any, False)
    Pass true to create an initial commit with README, .gitignore and LICENSE.


  gitignores (False, any, None)
    Desired language .gitignore templates to apply. Use the name of the templates. For example, 'Go' or 'Go,SublimeText'.


  license (False, any, default)
    Desired LICENSE template to apply. Use the name of the template. For example, 'Apache v2 License' or 'MIT License'.


  readme (False, any, None)
    Desired README template to apply. Use the name of the template.


  accessToken (True, any, None)
    The user Access Token









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create Repository
      gogs_createRepo:
        gogsURL: "http://gogs.local:3000/"
        organization: "acme"
        name: "Test Inventory"
        accessToken: "Token"



Return Values
-------------

  message (success, dict, )
    object




Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Renato Almeida de Oliveira (renato.a.oliveira@pm.me)

