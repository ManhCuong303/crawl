from lxml import html, etree
import csv, os, json
import random
import requests
import json
from exceptions import ValueError
from time import sleep
import urllib
import sys
from threading import Thread
import threading
import time
import datetime
import numpy as np
import re
import pymongo
from pymongo import MongoClient

ip_data = open('Chrome-user-agents.txt').read()

ip_list = json.loads(ip_data)

proxy = random.choice(ip_list)

sh = ip_list.index([{"https": "https://222.124.26.37:36910"},{"status": 0}])

print len(ip_list)

del ip_list[sh]
print len(ip_list)

fax = open('Chrome-user-agents.txt', 'w')
json.dump(ip_list, fax, indent=4)
fax.close()

# fax = open('Chrome-user-agents.txt', 'w')
# json.dumps(ip_list, fax, indent=4)

#
# db.getCollection('listAsinCache').aggregate([
# {
#     // only match documents that have this field
#     // you can omit this stage if you don't have missing fieldX
#     $match: {"ASIN": {$nin:[null]}}
# },
# {
#     $group: { "_id": "$ASIN", "doc" : {"$first": "$$ROOT"}}
# },
# {
#     $replaceRoot: { "newRoot": "$doc"}
# }
# ],
# {allowDiskUse:true})