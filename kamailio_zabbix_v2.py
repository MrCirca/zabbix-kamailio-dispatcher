#!/usr/bin/python2
import json
import requests
import sys
import subprocess
from pprint import pprint

data = subprocess.check_output(['cat', '/home/mrcirca/kamailio_json2.json']).decode()
nargs = len(sys.argv)
uris = []
kamailio_json = json.loads(data)
record_list = kamailio_json['result']['RECORDS']

if nargs == 1:
    for record  in record_list:
        id_number = record['SET']['ID']
        for target in record['SET']['TARGETS']:
            uri = target['DEST']['URI']
            socket = target['DEST']['ATTRS']['SOCKET'].split(':')[1]
            try:
               uris.append({"{#URI}": uri.split(':')[1], "{#ID}": id_number, "{#DESC}":
               uri.split('xdesc=')[1], "{#FLAG}": target['DEST']['FLAGS'], "{#SOCKET}":
               socket})
            except:
               uris.append({"{#URI}": uri.split(':')[1], "{#ID}": id_number, "{#DESC}": "None"})
    print(json.dumps({'data': uris}))



elif nargs == 3:
    for record in record_list:
        id_number = record['SET']['ID']
        for target in record['SET']['TARGETS']:
            uri = target['DEST']['URI']
            if sys.argv[1] == uri.split(':')[1] and sys.argv[2] == str(id_number):
                print(target['DEST']['FLAGS'])
elif nargs == 4:
    uri_arg = sys.argv[1]
    latency_arg = sys.argv[3]
    id_arg = sys.argv[2]
    for record in record_list:
        id_number = record['SET']['ID']
        for target in record['SET']['TARGETS']:
            latency = target['DEST']['LATENCY']
            uri = target['DEST']['URI']
            if uri_arg == uri.split(':')[1] and id_arg == str(id_number) and latency_arg == "max":
                print(latency['MAX'])
            elif uri_arg == uri.split(':')[1] and id_arg == str(id_number) and latency_arg == "avg":
                    print(latency['AVG'])
            elif  uri_arg== uri.split(':')[1] and id_arg == str(id_number) and latency_arg == "est":
                    print(latency['EST'])
            elif uri_arg == uri.split(':')[1] and id_arg == str(id_number) and latency_arg == "std":
                    print(latency['STD'])
            elif uri_arg == uri.split(':')[1] and id_arg == str(id_number) and latency_arg == "timeout":
                    print(latency['TIMEOUT'])
else:
    print("Wrong argument")
