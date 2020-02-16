#!/usr/bin/python

import requests
import json
import re

from ansible.module_utils.basic import *
from ansible.errors import *
from requests.auth import HTTPBasicAuth

def gogsSearch(module):
    user = module.params['user'] or module.params['organization']
    name = module.params['name']
    URL = module.params['gogsURL']
    Path = ""
    if (re.search("/$" , URL)):
        Path = URL
    else:
        Path = URL + "/"
    uri = Path + "api/v1/repos/" + user + "/" + name
    headers = {'Authorization': 'token ' + module.params['accessToken'] }
    request = requests.get(uri, headers=headers)
    return request

def gogsCreateRepo(module):
    name = module.params['name']
    resource = ""
    if module.params['user'] == None :
        org = module.params['organization']
        resource = "api/v1/org/%s/repos" % ( org )
    else:
        resource = "api/v1/user/repos"
    URL = module.params['gogsURL']
    Path = ""
    if (re.search("/$" , URL)):
        Path = URL + resource 
    else:
        Path = URL + "/" + resource 
    headers = {'Authorization': 'token ' + module.params['accessToken'] }
    parameters = ["name" , "description" , "private" , "gitignores" , "license" , "readme" ]
    payload = dict()
    for parameter in parameters:
        if module.params[parameter] != None :
            payload[parameter] = module.params[parameter]
    if module.params["autoInit"] != None :
        payload["auto_init"] =  module.params["autoInit"]
        payload["readme"] = module.params["readme"] or "Default"
    request = requests.post(Path, headers=headers , json=payload)
    request.raise_for_status()
    return request
    
    

def main():

    fields = {
        "gogsURL":    { "required": True , "type": "str" },
        "user":       { "type": "str"},
        "organization":  { "type": "str"},
        "name" : {"required": True, "type": "str"},
        "description" : {"required": False , "type": "str"},
        "private" : {"default":False, "type": "bool" },
        "autoInit" : {"default":True, "type": "bool" },
        "gitignores" : {"required": False , "type": "str"},
        "license" : {"required": False , "type": "str"},
        "readme" : {"required": False , "type": "str"},
        "accessToken":  {"required": True, "type": "str", "no_log": True },
    }

    module = AnsibleModule(argument_spec=fields , required_one_of=[ ['user' , 'organization']])
    result = dict(changed=False, warnings=list())
    try:
        response = gogsSearch(module)
        status = response.status_code
        if status == 404 :
            response = gogsCreateRepo(module)
            if response.status_code == 201 :
                result.update(changed=True , message = to_native(response.content))
            else :
                module.fail_json(msg = to_native(response.status_code))
        elif status == 200:
            result.update(changed=False )
        else:
            module.fail_json(msg = to_native(response))
    except Exception as e:
        module.fail_json(msg = to_native(e))
    
    module.exit_json(**result)


if __name__ == '__main__':
    main()


