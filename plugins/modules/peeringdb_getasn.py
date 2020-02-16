#!/usr/bin/python

import requests
import json

from ansible.module_utils.basic import AnsibleModule
from requests.auth import HTTPBasicAuth
ANSIBLE_METADATA = {
    'metadata_version': '1.0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: peeringdb_getasn

short_description: Searches in peeringDB database for an ASN policy and interfaces 

version_added: "0.0.1"

description:
    - "This modules encapsules peeringDB API to search for an specific ASN his interfaces and policy indormations"

options:
    asn:
        description:
          - "The searched ASN"
        required: true
    username:
        description:
          - "Your peeringDB User"
        required: false
    password:
        description:
          - "Your peeringDB password"
        required: false
    ix-id:
        description:
          - "The peeringDB IXP ID"
        required: false
    ix-name:
        description:
          - "The peerigDB IXP Name"
        required: false
author:
    - Renato Almeida de Oliveira (renato.a.oliveira@pm.me)
'''

EXAMPLES = '''
# Get ASN 15169 data on IXP with id 171
- name: Search ASN 15169
  peeringdb_getasn:
    asn: 15169
    ix-id: 171
'''

RETURN = '''
message:
  ASN:
    - description: "The target ASN"
  info_ipv6: 
    - description: "Is True if the ASN uses IPv6"
  info_prefixes4:
    - description: "The number of IPv4 prefixes the ASN announces"
  info_prefixes6:
    - description: "The number of IPv4 prefixes the ASN announces"
  info_unicast:
    - description: "Is True if the ASN uses IPv4"
  interfaces:
    - description: "List with the ASN interfaces information"
    - objects: 
      - ipaddr4: "The interface IPv4 address"
        ipaddr6: "The interface IPv4 address"
        speed: : "The interface speed"
  irr_as_set:
    - description: "The IRR AS-SET"
  poc_set:
    - description: "Object with contact information"
'''


def getASNID(asn, username=None, password=None):

    if (username is not None) and (password is not None):
        request = requests.get("https://www.peeringdb.com/api/net?asn=" + str(asn),
                               auth=HTTPBasicAuth(username, password))
    else:
        request = requests.get(
            "https://www.peeringdb.com/api/net?asn=" + str(asn))

    request.raise_for_status()
    response = json.loads(request.text)
    result = None
    for data in response["data"]:
        if data["asn"] == int(asn):
            result = data["id"]
            break
    if result is not None:
        return result
    else:
        raise NameError('Unknown ASN')


def getASNData(asn, username=None, password=None):

    asnId = getASNID(asn)

    if (username is not None) and (password is not None):
        asnId = getASNID(asn, username, password)
        request = requests.get("https://www.peeringdb.com/api/net/" + str(asnId),
                               auth=HTTPBasicAuth(username, password))
    else:
        asnId = getASNID(asn)
        request = requests.get(
            "https://www.peeringdb.com/api/net/" + str(asnId))

    request.raise_for_status()
    response = json.loads(request.text)
    return response["data"][0]


def pasrseASNData(asn, username=None, password=None, ixId=None, ixName=None):
    keys = ["info_prefixes4", "info_prefixes6",
            "poc_set", "info_unicast", "info_ipv6"]
    data = getASNData(asn, username, password)
    output = {}
    ixOutput = []
    irrData = []
    output["ASN"] = asn
    for key in keys:
        if key in data:
            output[key] = data[key]
    if "irr_as_set" in data:
        if data["irr_as_set"] == "":
            irrData = []
        else:
            irrDataSet = data["irr_as_set"].split(" ")

            for irrAsSet in irrDataSet:
                irrRepoSet = irrAsSet.split("::")
                if len(irrRepoSet) == 1:
                    irrData.append(irrRepoSet[0])
                else:
                    irrData.append(irrRepoSet[1])
    if "netixlan_set" in data:
        ixFilter = None
        if ixName is not None:
            ixFilter = "name"
        if ixId is not None:
            ixFilter = "ix_id"
        inputIxData = ixId or ixName
        if ixFilter is not None:
            ixSet = data["netixlan_set"]
            ixOutput = []
            interfaceData = {}
            for ix in ixSet:
                if ix[ixFilter] == inputIxData:
                    if "ipaddr4" in ix:
                        interfaceData["ipaddr4"] = ix["ipaddr4"]
                    if "ipaddr6" in ix:
                        interfaceData["ipaddr6"] = ix["ipaddr6"]
                    if "speed" in ix:
                        interfaceData["speed"] = ix["speed"]
                    ixOutput.append(interfaceData)
    if ixOutput != []:
        output["interfaces"] = ixOutput
    output["irr_as_set"] = irrData
    return output


def main():

    fields = {
        "asn":       {"required": True,  "type": "int"},
        "username":  {"required": False, "type": "str"},
        "password":  {"required": False, "type": "str", "no_log": True},
        "ix-id":     {"required": False, "type": "int"},
        "ix-name":   {"required": False, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    response = pasrseASNData(module.params['asn'], module.params['username'],
                             module.params['password'], module.params['ix-id'], module.params['ix-name'])
    module.exit_json(changed=False, message=response)


if __name__ == '__main__':
    main()
