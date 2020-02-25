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

DOCUMENTATION = """
module: peeringdb_prospect

short_description: Searches for common IXP

version_added: "0.0.1"

description:
    - "This modules uses peeringDB API to lookup for IXP that dst-ASN has in commoon with src-ASN"
    - "Providing username and password allows peeringDB to provide restricted information on the query"

options:
    src-asn:
        description:
            - "The source ASN you whant to lookup for matches on IXP"
        required: true
    dst-asn:
        description:
            - "The destination ASN you whant to lookup for matches on IXP"
        required: true
    username:
        description:
            - "The peeringdb Username"
        required: false
    password:
        description:
            - "The peeringDB password"
        required: false
author:
    - Renato Almeida de Oliveira (renato.a.oliveira@pm.me)
"""

EXAMPLES = """
- name: Get ASN Data
  peeringdb_prospect:
    dst-asn: 15169
    src-asn: 2906
"""

RETURN = """
object:
    description: object representing ASN data
    returned: success
    type: dict
"""

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


def pasrseASNData(srcAsn, dstAsn, username=None, password=None):
    srcAsnData = getASNData(srcAsn, username, password)
    srcIxLocations = {}
    output = []
    for ixlan in srcAsnData["netixlan_set"]:
        if not (ixlan["ix_id"] in srcIxLocations):
            srcIxLocations[ixlan["ix_id"]] = ixlan["name"]
    dstOutput = {}
    commomIxLocations = []
    dstAsnData = getASNData(dstAsn, username, password)
    dstIxLocations = {}
    for ixlan in dstAsnData["netixlan_set"]:
        if not (ixlan["ix_id"] in dstIxLocations):
            dstIxLocations[ixlan["ix_id"]] = ixlan["name"]
    for ixId in srcIxLocations:
        matchLocation = {}
        if ixId in dstIxLocations:
            matchLocation = {"id": ixId, "name": dstIxLocations[ixId]}
            commomIxLocations.append(matchLocation)
    if commomIxLocations != []:
        dstOutput[dstAsn] = {
            "name": dstAsnData["name"],
            "IXs": commomIxLocations,
            "poc_set": dstAsnData["poc_set"]
        }
        output.append(dstOutput)
    return output


def main():

    fields = {
        "src-asn":   {"required": True,  "type": "int"},
        "dst-asn":   {"required": True,  "type": "int"},
        "username":  {"required": False, "type": "str"},
        "password":  {"required": False, "type": "str", "no_log": True}
    }
    module = AnsibleModule(argument_spec=fields)
    response = pasrseASNData(module.params['src-asn'], module.params['dst-asn'],
                             module.params['username'], module.params['password'])
    module.exit_json(changed=False, message=response)


if __name__ == '__main__':
    main()
