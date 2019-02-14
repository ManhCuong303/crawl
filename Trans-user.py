import json
import urllib
import numpy as np
import re

ipdata = []
def aki():
    f = open('Chrome-user-agents.txt', 'r')
    data = f.readlines()
    for line in data:
        xx =  "https://" + line
        xx = re.sub('\n+', '', xx)
        print xx
        ipdata.append({"https":xx})
    fa = open('Chrome-user-agents.json', 'w')
    json.dump(ipdata, fa, indent=4)
    fa.close()
    f.close()


aki()