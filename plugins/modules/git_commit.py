#!/usr/bin/python

from ansible.errors import AnsibleError
from ansible.module_utils.basic import to_native, AnsibleModule
import datetime
ANSIBLE_METADATA = {
    'metadata_version': '1.0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: git_commit

short_description: Makes git commit on repository

version_added: "0.0.1"

description:
    - "This module runs git status and if there are any changes on the repository makes git add * ana git commit"

options:
    path:
        description:
            - The repository path
        required: true
    commitMessage:
        description:
            - Sets the commit message, if none uses timestamp
        required: false
requirements:
    - git>=1.7.1 (the command line tool)
author:
    - Renato Almeida de Oliveira (renato.a.oliveira@pm.me)
'''

EXAMPLES = '''
- name: Commit repo
  git_commit:
    path: /home/repository

- name: Commit with message
  git_commit:
    path: /home/repository
    commitMessage: "Commit executed by Ansible"
'''

RETURN = '''
message:
  description: object
  returned: success
  type: dict
'''


def git_status(module, git_path, repo_path):
    cmd = "%s status -s" % (git_path)
    rc, stdout, stderr = module.run_command(cmd, cwd=repo_path)
    if stderr != "":
        raise AnsibleError(" git_clone error: %s " % to_native(stderr))
    return stdout


def git_commit(module, git_path, repo_path, commitMsg):
    cmd = "%s add * " % (git_path)
    rc, stdout, stderr = module.run_command(cmd, cwd=repo_path)
    if stderr != "":
        raise AnsibleError(" git add error: %s " % to_native(stderr))
    cmd = "%s commit -m \"%s\"" % (git_path, commitMsg)
    rc, stdout, stderr = module.run_command(cmd, cwd=repo_path)
    if stderr != "":
        raise AnsibleError(" git commit error: %s " % to_native(stderr))
    return stdout


def main():

    fields = {
        "path":       {"required": True,  "type": "str"},
        "commitMessage":  {"required": False, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    path = module.get_bin_path('git', True)
    result = dict(changed=False, warnings=list())
    try:
        response = git_status(module, path, module.params['path'])
        if response == "":
            result.update(changed=False)
        else:
            msg = module.params['commitMessage'] or datetime.datetime.now()
            commitResponse = git_commit(
                module, path, module.params['path'], msg)
            result.update(changed=True, message=to_native(commitResponse))
    except Exception as e:
        module.fail_json(msg=to_native(e))
    module.exit_json(**result)


if __name__ == '__main__':
    main()
