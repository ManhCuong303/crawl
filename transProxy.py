import json
import urllib
import numpy as np
import re
import time
import datetime
import pymongo
from pymongo import MongoClient

ipdata = []
aka = {}
client = MongoClient('localhost', 27017)
db = client.dataAsin
dataAsin = db['ipUSList']
dataAsin.remove({})
def aki():
    f = open('ipUS.txt', 'r')
    data = f.readlines()
    print len(data)
    id = 0
    for line in data:
        if len(line) > 5:
            xx = "https://" + line
            yy = "http://" + line
            xx = re.sub('\n+', '', xx)
            yy = re.sub('\n+', '', yy)
            aka = {"https": xx,"http": yy}
            fid = {'data':[aka,{'status':0}]}
            print xx , yy
            showcoll = dataAsin.count_documents(fid)
            if showcoll == 0 :
                fid = {'data': [aka, {'status': 0}],'id':id,'geted':'false','dateGet':int(time.mktime(time.localtime())),'turn':0}
                dataAsin.insert_one(fid)
                id += 1
            else:
                print aka
aki()