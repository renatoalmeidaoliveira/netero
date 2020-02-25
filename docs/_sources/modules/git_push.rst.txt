
git_push -- Makes git push on repository
========================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module runs git status -sb and if there are any changes on the repository make git push

This module assumes that Ansible server and the Git Server can connect



Requirements
------------
The below requirements are needed on the host that executes this module.

- git>=1.7.1 (the command line tool)



Parameters
----------

  path (True, any, None)
    The repository path









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Push repo
      git_push:
        path: /home/repository



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

