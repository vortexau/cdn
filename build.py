#!/usr/bin/env python3

import yaml
import requests
import re

providers = "providers.yaml"
output = "cdns.yaml"

with open(providers, 'r') as stream:
    try:
        cdns = yaml.safe_load(stream)
        cdnout = {}
        for cdn,urls in cdns.items():
            for url in urls:
                #print(url)
                try:
                    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
                    cdndata = requests.get(url, headers=headers)
                    matches = re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,3}", cdndata.text, re.MULTILINE)
                    thiscdn = set() 
                    for match in matches:
                        thiscdn.add(match)

                    if len(thiscdn) > 0:
                        cdnout[cdn] = list(thiscdn)
                except Exception as e:
                    print("Exception {}".format(e))


    except yaml.YAMLError as exc:
        print(exc)

with open(output, 'w') as outfile:
    yamldata = yaml.dump(cdnout, allow_unicode=True)
    outfile.write(yamldata)
