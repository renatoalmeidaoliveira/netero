import json
import datetime
import re

from ansible.module_utils.basic import *
from ansible.errors import *

def git_status(module , git_path , repo_path):
    cmd = "%s status -sb" % (git_path )
    rc , stdout , stderr = module.run_command(cmd , cwd=repo_path)
    if stderr != "" :
        raise AnsibleError(" git_clone error: %s " % to_native(stderr) )
    return stdout
def git_push(module , git_path, repo_path ):
    cmd = "%s push --porcelain" % (git_path )
    rc , stdout , stderr = module.run_command(cmd , cwd=repo_path)
    if stderr != "" :
        errorSanitized = re.sub(r'\/\/.*\:.*@' , '//***@' , stderr )
        raise AnsibleError(" git push error: %s " % errorSanitized )
    return stdout


def main():

    fields = {
        "path":       {"required": True,  "type": "str"},
        "key":  {"required": False, "type": "str"},
        "username":     {"required": False, "type": "str"},
        "password":   {"required": False, "type": "str" , "no_log": True }
    }
    module = AnsibleModule(argument_spec=fields)
    path = module.get_bin_path('git' , True)
    result = dict(changed=False, warnings=list())
    try:
        response = git_status(module , path , module.params['path'])
        modified =  re.search("\[ahead \d+\]" , response)
        if modified == None :
            result.update(changed=False)
        else :
            pushResponse = git_push(module , path , module.params['path'])
            result.update(changed=True , message = to_native(pushResponse))
    except Exception as e :
        module.fail_json(msg= to_native(e))
    module.exit_json(**result)

if __name__ == '__main__':
    main()

