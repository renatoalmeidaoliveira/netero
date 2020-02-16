#!/usr/bin/python

import requests
import json

from ansible.module_utils.basic import *
from requests.auth import HTTPBasicAuth


def getASNID(asn , username=None , password=None) :

    if (username != None ) and (password != None) :
        request = requests.get("https://www.peeringdb.com/api/net?asn=" + str(asn) ,
            auth=HTTPBasicAuth(username , password  ))
    else:
        request = requests.get("https://www.peeringdb.com/api/net?asn=" + str(asn))

    request.raise_for_status()
    response = json.loads(request.text)
    result = None
    for data in response["data"] :
        if data["asn"] == int(asn) :
            result = data["id"]
            break
    if result != None :
        return result
    else:
        raise NameError('Unknown ASN')

def getASNData(asn, username=None , password=None):

    asnId = getASNID(asn)

    if (username != None ) and (password != None) :
        asnId = getASNID(asn , username , password)
        request = requests.get("https://www.peeringdb.com/api/net/" + str(asnId) ,
            auth=HTTPBasicAuth(username , password  ))
    else:
        asnId = getASNID(asn)
        request = requests.get("https://www.peeringdb.com/api/net/" + str(asnId))

    request.raise_for_status()
    response = json.loads(request.text)
    return response["data"][0]

def pasrseASNData(srcAsn , dstAsn , username=None , password=None ):
    srcAsnData = getASNData(srcAsn , username , password)
    srcIxLocations = {}
    output = []
    for ixlan in srcAsnData["netixlan_set"] :
        if not (ixlan["ix_id"] in srcIxLocations) :
            srcIxLocations[ixlan["ix_id"]] = ixlan["name"]
    dstOutput = {}
    commomIxLocations = []
    dstAsnData = getASNData(dstAsn , username , password)
    dstIxLocations = {}
    for ixlan in dstAsnData["netixlan_set"] :
        if not (ixlan["ix_id"] in dstIxLocations) :
            dstIxLocations[ixlan["ix_id"]] = ixlan["name"]
    for ixId in srcIxLocations :
        matchLocation = {}
        if ixId in dstIxLocations :
            matchLocation = { "id" : ixId , "name" : dstIxLocations[ixId] }
            commomIxLocations.append(matchLocation)
    if commomIxLocations != [] :
        dstOutput[dstAsn] = {
            "IXs" : commomIxLocations , 
            "poc_set" : dstAsnData["poc_set"]
        }
        output.append(dstOutput)
    return output





def main():

    fields = {
        "src-asn":   {"required": True,  "type": "int"},
        "dst-asn":   {"required": True,  "type": "int"},
        "username":  {"required": False, "type": "str"},
        "password":  {"required": False, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    response = pasrseASNData(module.params['src-asn'] , module.params['dst-asn'] ,
        module.params['username'] , module.params['password'] )
    module.exit_json(changed=False, message=response)


if __name__ == '__main__':
    main()
