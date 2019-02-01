import json
import urllib
import numpy as np
import re

ipdata = []
def aki():
    f = open('list-proxy.txt', 'r')
    data = f.readlines()
    for line in data:
        if len(line) > 5 :
            xx =  "https://" + line
            xx = re.sub('\n+', '', xx)
            print xx,len(line)
            ipdata.append({"https":xx})
    fa = open('ip_list.json', 'w')
    json.dump(ipdata, fa, indent=4)
    fa.close()
    f.close()


aki()