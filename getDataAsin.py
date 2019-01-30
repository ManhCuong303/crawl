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
import numpy as np
import re
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dataAsin
coll = db['testColl']

this = sys.modules[__name__] # this is now your current namespace
extracted_data = []
fail_getByAsin = []
count_asin_re = []
textC = 'ShippingWeight:,4.8'

json_data = open('Chrome-user-agents.json').read()
headers_list = json.loads(json_data)
ip_data = open('ip_list.json').read()
ip_list = json.loads(ip_data)

def ReadAsin(dataAsins):
    headers = random.choice(headers_list)
    proxy = random.choice(ip_list)
    for listAsin in dataAsins:
        reGetTitle(listAsin)


def getDataOk(html):
    return 'ok'

def reGetTitle(i):
    url = "http://www.amazon.com/dp/" + i
    headers = random.choice(headers_list)
    proxy = random.choice(ip_list)
    try:
        page = requests.get(url, headers=headers, proxies=proxy, timeout=30)
        try:
            doc = html.fromstring(page.content)

            XPATH_CHECK = '//*[@id="detailBullets_feature_div"]'

            RAW_CHECK = doc.xpath(XPATH_CHECK)

            RAW_CHECK_cache = ''

            # if not ORIGINAL_PRICE:
            #     ORIGINAL_PRICE = SALE_PRICE

            if len(RAW_CHECK) == 0:
                RAW_CHECK = doc.xpath('//*[@id="detail-bullets"]')
            for article in RAW_CHECK:
                RAW_CHECK_cache = RAW_CHECK_cache + etree.tostring(article, pretty_print=True)

            RAW_CHECK = re.sub('<[^<]+?>', '', RAW_CHECK_cache)
            RAW_CHECK = RAW_CHECK.replace(" ", "")
            RAW_CHECK = re.sub('\n+', ',', RAW_CHECK)



            if RAW_CHECK.find(textC) != -1:
                XPATH_PRICE = '//*[@id="priceblock_ourprice"]/text()'
                XPATH_BRAN = '//*[@id="bylineInfo"]/text()'
                XPATH_NAME = '//h1[@id="title"]//text()'
                XPATH_RANK = '//*[@id="SalesRank"]/text()'

                RAW_DEC = doc.xpath('//*[@id="featurebullets_feature_div"]')
                RAW_IMG = doc.xpath('//*[@id="landingImage"]/@data-old-hires')

                RAW_DEC_cache = ''
                for rawdec in RAW_DEC:
                    RAW_DEC_cache = RAW_DEC_cache + etree.tostring(rawdec, pretty_print=True)
                RAW_DEC = RAW_DEC_cache

                RAW_PRICE = doc.xpath(XPATH_PRICE)
                RAW_NAME = doc.xpath(XPATH_NAME)
                RAW_NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
                RAW_RANK = doc.xpath(XPATH_RANK)
                if len(RAW_RANK) == 0 :
                    RAW_RANK = 'no rank'
                else:
                    RAW_RANK = RAW_RANK[1].split()
                    RAW_RANK = RAW_RANK[0]
                RAW_BRAN = doc.xpath(XPATH_BRAN)

                if len(RAW_BRAN) == 0:
                    RAW_BRAN = doc.xpath('//*[@id="brand"]/@href')
                    RAW_BRAN = RAW_BRAN[0].split("/",2)
                    RAW_BRAN[0] = RAW_BRAN[1]

                if len(RAW_PRICE) == 0:
                    RAW_PRICE = ['no']
                print '====GOOD====',RAW_BRAN
                data = {
                    'ASIN': i,
                    'NAME': RAW_NAME,
                    'RANK': RAW_RANK,
                    'BRAN': RAW_BRAN[0],
                    'PRICE': RAW_PRICE[0],
                    'DEC':RAW_DEC,
                    'IMG':RAW_IMG[0]
                }
                coll.insert_one(data)

            # for article in RAW_CHECK:


        except Exception as e:
            print 'xx', e, url
            kap = {
                'head': headers,
                'proxy': proxy,
                'url': url,
                'status': e,
            }
            fail_getByAsin.append(kap)
            return reGetTitle(i)
        count_asin_re.append(url)
        print "===Request=== ",len(count_asin_re) ,url
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return  reGetTitle(i)

if __name__ == "__main__":
    iz = 90
    with open('data2.txt', mode='r') as f:
        result = f.readlines()
        for xx in xrange(0,len(result)):
            result[xx] = re.sub('\n+', '', result[xx])
    AsinList = np.array_split(result, iz)
    threads = []
    try:
        for n in range(0, iz):
            name ='t'+ str(n)
            threads.append(threading.Thread(name=name,target=ReadAsin, args=(AsinList[n],)))
            threads[-1].start()  # start the thread we just created
        for t in threads:
            t.join()



        print 'DONE !'
    except requests.exceptions.RequestException as e:
        print ("error",e)




