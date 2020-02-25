#!/usr/bin/python

import requests
import json
import re

from ansible.module_utils.basic import AnsibleModule, to_native
from requests.auth import HTTPBasicAuth

ANSIBLE_METADATA = {
    'metadata_version': '1.0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: gogs_createrepo

short_description: Create a repository on Gogs

version_added: "0.0.1"

description:
    - "This module encapusles Gogs API to create a repository"

options:
    gogsURL:
        description:
            - "The Gogs Server URL"
        required: true
    user:
        description:
            - "The user that owns the repository, This argument is mutually
        exclusive with organization."
        required: false
    organization:
        description:
             - "The organization that owns the repository, This argument is mutually
        exclusive with user."
        required: false
    name:
        description:
           - "The repository name"
        required: true
    description:
        description:
            - "A short description of the repository"
        required: false
    private:
        description:
           - "Either true to create a private repository, or false to create a public one"
        default: false
        required: false
    autoInit:
        description:
           - "Pass true to create an initial commit with README, .gitignore and LICENSE."
        default: false
        required: false
    gitignores:
        description:
            - "Desired language .gitignore templates to apply. Use the name of the templates. For example, 'Go' or 'Go,SublimeText'."
        required: false
    license:
        description:
            - "Desired LICENSE template to apply. Use the name of the template. For example, 'Apache v2 License' or 'MIT License'."
        default: default
        required: false
    readme:
        description:
            - "Desired README template to apply. Use the name of the template."
        required: false
    accessToken:
        description: 
            - "The user Access Token"
        required: true


author:
    - Renato Almeida de Oliveira (renato.a.oliveira@pm.me)
'''

EXAMPLES = '''
- name: Create Repository
  gogs_createRepo:
    gogsURL: "http://gogs.local:3000/"
    organization: "acme"
    name: "Test Inventory"
    accessToken: "Token"
'''

RETURN = '''
message:
  description: object
  returned: success
  type: dict
'''


def gogsSearch(module):
    user = module.params['user'] or module.params['organization']
    name = module.params['name']
    URL = module.params['gogsURL']
    Path = ""
    if (re.search("/$", URL)):
        Path = URL
    else:
        Path = URL + "/"
    uri = Path + "api/v1/repos/" + user + "/" + name
    headers = {'Authorization': 'token ' + module.params['accessToken']}
    request = requests.get(uri, headers=headers)
    return request


def gogsCreateRepo(module):
    name = module.params['name']
    resource = ""
    if module.params['user'] == None:
        org = module.params['organization']
        resource = "api/v1/org/%s/repos" % (org)
    else:
        resource = "api/v1/user/repos"
    URL = module.params['gogsURL']
    Path = ""
    if (re.search("/$", URL)):
        Path = URL + resource
    else:
        Path = URL + "/" + resource
    headers = {'Authorization': 'token ' + module.params['accessToken']}
    parameters = ["name", "description", "private",
                  "gitignores", "license", "readme"]
    payload = dict()
    for parameter in parameters:
        if module.params[parameter] != None:
            payload[parameter] = module.params[parameter]
    if module.params["autoInit"] != None:
        payload["auto_init"] = module.params["autoInit"]
        payload["readme"] = module.params["readme"] or "Default"
    request = requests.post(Path, headers=headers, json=payload)
    request.raise_for_status()
    return request


def main():

    fields = {
        "gogsURL":    {"required": True, "type": "str"},
        "user":       {"type": "str"},
        "organization":  {"type": "str"},
        "name": {"required": True, "type": "str"},
        "description": {"required": False, "type": "str"},
        "private": {"default": False, "type": "bool"},
        "autoInit": {"default": True, "type": "bool"},
        "gitignores": {"required": False, "type": "str"},
        "license": {"required": False, "type": "str"},
        "readme": {"required": False, "type": "str"},
        "accessToken":  {"required": True, "type": "str", "no_log": True},
    }

    module = AnsibleModule(argument_spec=fields, required_one_of=[
                           ['user', 'organization']])
    result = dict(changed=False, warnings=list())
    try:
        response = gogsSearch(module)
        status = response.status_code
        if status == 404:
            response = gogsCreateRepo(module)
            if response.status_code == 201:
                result.update(
                    changed=True, message=to_native(response.content))
            else:
                module.fail_json(msg=to_native(response.status_code))
        elif status == 200:
            result.update(changed=False)
        else:
            module.fail_json(msg=to_native(response))
    except Exception as e:
        module.fail_json(msg=to_native(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
