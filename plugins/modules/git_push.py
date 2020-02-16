import json
import datetime
import re

from ansible.module_utils.basic import *
from ansible.errors import *

ANSIBLE_METADATA = {
    'metadata_version': '1.0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: git_push

short_description: Makes git push on repository

version_added: "0.0.1"

description:
    - "This module runs git status -sb and if there are any changes on the repository make git push"
    - "This module assumes that Ansible server and the Git Server can connect"

options:
    path:
        description:
            - The repository path
        required: true

requirements:
    - git>=1.7.1 (the command line tool)
author:
    - Renato Almeida de Oliveira (renato.a.oliveira@pm.me)
'''

EXAMPLES = '''
# Push changes to the repository
- name: Push repo
  git_push:
    path: /home/repository
'''


def git_status(module, git_path, repo_path):
    cmd = "%s status -sb" % (git_path)
    rc, stdout, stderr = module.run_command(cmd, cwd=repo_path)
    if stderr != "":
        raise AnsibleError(" git_clone error: %s " % to_native(stderr))
    return stdout


def git_push(module, git_path, repo_path):
    cmd = "%s push --porcelain" % (git_path)
    rc, stdout, stderr = module.run_command(cmd, cwd=repo_path)
    if stderr != "":
        errorSanitized = re.sub(r'\/\/.*\:.*@', '//***@', stderr)
        raise AnsibleError(" git push error: %s " % errorSanitized)
    return stdout


def main():

    fields = {
        "path":       {"required": True,  "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    path = module.get_bin_path('git', True)
    result = dict(changed=False, warnings=list())
    try:
        response = git_status(module, path, module.params['path'])
        modified = re.search("\[ahead \d+\]", response)
        if modified == None:
            result.update(changed=False)
        else:
            pushResponse = git_push(module, path, module.params['path'])
            result.update(changed=True, message=to_native(pushResponse))
    except Exception as e:
        module.fail_json(msg=to_native(e))
    module.exit_json(**result)


if __name__ == '__main__':
    main()
