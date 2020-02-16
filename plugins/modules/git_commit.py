#!/usr/bin/python

import json
import datetime

from ansible.module_utils.basic import *
from ansible.errors import *

def git_status(module , git_path , repo_path):
    cmd = "%s status -s" % (git_path )
    rc , stdout , stderr = module.run_command(cmd , cwd=repo_path)
    if stderr != "" :
        raise AnsibleError(" git_clone error: %s " % to_native(stderr) )        
    return stdout
def git_commit(module , git_path, repo_path , commitMsg ):
    cmd = "%s add * " % (git_path )
    rc , stdout , stderr = module.run_command(cmd , cwd=repo_path)
    if stderr != "" :
        raise AnsibleError(" git add error: %s " % to_native(stderr) )
    cmd = "%s commit -m \"%s\"" % (git_path , commitMsg )
    rc , stdout , stderr = module.run_command(cmd , cwd=repo_path)
    if stderr != "" :
        raise AnsibleError(" git commit error: %s " % to_native(stderr) )
    return stdout


def main():

    fields = {
        "path":       {"required": True,  "type": "str"},
        "commitMessage":  {"required" : False , "type": "str" },
        "remote":  {"required": False, "type": "str"},
        "key":  {"required": False, "type": "str"},
        "username":     {"required": False, "type": "str"},
        "password":   {"required": False, "type": "str" , "no_log": True }
    }
    module = AnsibleModule(argument_spec=fields)
    path = module.get_bin_path('git' , True)
    result = dict(changed=False, warnings=list())
    try:
        response = git_status(module , path , module.params['path'])
        if response == "" :
            result.update(changed=False)
        else :
            msg = module.params['commitMessage'] or datetime.datetime.now()
            commitResponse = git_commit(module , path , module.params['path'], msg)
            result.update(changed=True , message = to_native(commitResponse))
    except Exception as e :
        module.fail_json(msg= to_native(e))
    module.exit_json(**result)

if __name__ == '__main__':
    main()


