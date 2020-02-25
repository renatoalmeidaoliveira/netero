
git_commit -- Makes git commit on repository
============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module runs git status and if there are any changes on the repository makes git add * ana git commit



Requirements
------------
The below requirements are needed on the host that executes this module.

- git>=1.7.1 (the command line tool)



Parameters
----------

  path (True, any, None)
    The repository path


  commitMessage (False, any, None)
    Sets the commit message, if none uses timestamp









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Commit repo
      git_commit:
        path: /home/repository

    - name: Commit with message
      git_commit:
        path: /home/repository
        commitMessage: "Commit executed by Ansible"



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

