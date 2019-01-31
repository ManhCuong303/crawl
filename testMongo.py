import pymongo
from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client.dataAsin
listAsinReal = db['listAsinReal']
listAsinCache = db['listAsinCache']

post = {"author": "Mike",
        "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

# coll.insert_one(post)
kake = []
listAsinReal = listAsinReal.find({})
listAsinCache = listAsinCache.count_documents({})

# for real in listAsinReal:
for real in listAsinReal:
    realA = real['ASIN']
    if kake.count(realA) == 0:
        kake.append(realA)
print len(kake)

print 'listAsinReal',listAsinReal,'listAsinCache',listAsinCache

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