import json
import urllib
import numpy as np
import re
import pymongo
from pymongo import MongoClient

ipdata = []
aka = {}
client = MongoClient('localhost', 27017)
db = client.dataAsin
dataAsin = db['iplist']

def aki():
    f = open('list-proxy.txt', 'r')
    data = f.readlines()
    print len(data)
    id = 0
    for line in data:
        if len(line) > 5:
            xx = "https://" + line
            xx = re.sub('\n+', '', xx)
            aka = {"https": xx}
            fid = {'data':[aka,{'status':0}]}
            showcoll = dataAsin.count_documents(fid)
            if showcoll == 0 :
                fid = {'data': [aka, {'status': 5}],'id':id}
                dataAsin.insert_one(fid)
                id += 1
                if i == 0:
                    print i
            else:
                print aka

aki()