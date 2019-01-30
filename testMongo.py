import pymongo
from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client.dataAsin
coll = db['testColl']

post = {"author": "Mike",
        "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

# coll.insert_one(post)
showcoll = coll.count_documents({})
print showcoll
