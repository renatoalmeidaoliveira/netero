#!/usr/bin/python
#  Netero an Ansible collection for network automation.
#  Copyright (C) 2020  Renato Almeida de Oliveira <renato.almeida.oliveira@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from ansible.errors import AnsibleError
from ansible.module_utils.basic import to_native, AnsibleModule
import json
ANSIBLE_METADATA = {
    'metadata_version': '1.0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: irr_prefix

short_description: Generater IRR prefix-list

version_added: "0.0.1"

description:
    - "This modules runs bgpq3 to generate model based prefix-list"

options:
    asn32Safe:
        description:
            - "assume that your device is asn32-safe"
        required: false
        default: false
    IPv:
        description:
            - "IP protocol version"
        required: true
        choices: [ 4 , 6]
    aggregate:
        description:
            - "If true aggregate the prefix"
        required: false
        default: false
    asSet:
        descriptio:
            - "The ASN IRR AS-SET"
        required: true
requirements:
    - bgpq3
author:
    - Renato Almeida de Oliveira (renato.a.oliveira@pm.me)
'''

EXAMPLES = '''
- name: Get prefix-list
  irr_prefix:
    asn32_safe: true
    IPv: 4
    as-set: AS1234
'''

RETURN = '''
message:
  description: object containing the IRR prefixes
  returned: success
  type: dict
'''


def bgpq3Query(module, path):
    args = module.params["IPv"]
    if module.params["asn32Safe"]:
        args = args + "3"
    if module.params["aggregate"]:
        args = args + "A"
    if module.params["host"]:
        args = "%s -h %s" % (args, module.params["host"])
    cmd = "%s -j%s -l irr_prefix %s" % (path, args, module.params["asSet"])
    rc, stdout, stderr = module.run_command(cmd)
    if stderr != "":
        raise AnsibleError(" bgpq3 error: %s " % to_native(stderr))
    data = json.loads(stdout)
    fields = ['prefix', 'exact', 'less-equal', 'greater-equal']
    output = {"irrPrefix": []}
    for prefixData in data["irr_prefix"]:
        prefixObject = {}
        for field in fields:
            if field in prefixData:
                fieldName = field
                if field == "less-equal":
                    fieldName = "lessEqual"
                if field == "greater-equal":
                    fieldName = "greaterEqual"
                prefixObject[fieldName] = str(prefixData[field])
        output["irrPrefix"].append(prefixObject)
    return output


def main():

    fields = {
        "asn32Safe":    {"default": False, "type": "bool"},
        "IPv":          {"required": True, "type": "str", "choices": ['4', '6']},
        "aggregate":    {"default": False, "type": "bool"},
        "asSet":        {"required": True, "type": "str"},
        "host":         {"required": False, "type": "str"}

    }
    module = AnsibleModule(argument_spec=fields)
    result = dict(changed=False, warnings=list())
    try:
        path = module.get_bin_path('bgpq4', False) or module.get_bin_path('bgpq3', False)
        if path is None:
            raise AnsibleError("BGPq3 ou BGPq4 not found")
        response = bgpq3Query(module, path)
        result.update(changed=True, message=response)
    except Exception as e:
        module.fail_json(msg=to_native(e))
    module.exit_json(**result)


if __name__ == '__main__':
    main()
