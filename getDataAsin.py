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

client = MongoClient('localhost', 27017)
db = client.dataAsin
dataAsin = db['listAsinCache']
dataFromAsin = db['dataFromAsin']
rankForAsin = db['rankForAsin']
iplist = db['iplist']

this = sys.modules[__name__] # this is now your current namespace
extracted_data = []
fail_getByAsin = []
count_asin_re = []
textFind = 'ShippingWeight:,4.8'

json_data = open('Chrome-user-agents.json').read()
headers_list = json.loads(json_data)


def ReadAsin(dataAsins):
    for listAsin in dataAsins:
        reGetTitle( listAsin['ASIN'])


def getDataOk(html):
    return 'ok'

def reGetTitle(i):
    url = "http://www.amazon.com/dp/" + i
    countIplist = iplist.count({})
    headers = random.choice(headers_list)
    idRandom = random.randint(0,countIplist)
    Getproxy = list(iplist.find({'id':idRandom}))

    proxy = Getproxy[0]['data']
    proxyAdd = proxy


    if proxy[1]['status'] + 1 > 4:
        # iplist.remove({'id':idRandom})
        reGetTitle(i)
    else:
        proxy[1]['status'] = proxy[1]['status'] + 1
        iplist.update({'id': idRandom}, {'$set': {"data": proxy}})
        try:
            print '-----------',proxy[0]
            page = requests.get(url, headers=headers, proxies=proxy[0], timeout=30)
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

                if RAW_CHECK.find(textFind) != -1:
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
                        RAW_RANK = '00'
                    else:
                        RAW_RANK = RAW_RANK[1].split()
                        RAW_RANK = RAW_RANK[0]

                    RAW_BRAN = doc.xpath(XPATH_BRAN)

                    RAW_RANK = RAW_RANK.lstrip('#')
                    try:
                        if RAW_CHECK.find('DatefirstlistedonAmazon'):
                            BRAN_DATE = doc.xpath('//*[@id="detailBullets_feature_div"]/ul/li[5]/span/span[2]')
                            BRAN_DATE_cache = ''
                            for zz in BRAN_DATE:
                                BRAN_DATE_cache = BRAN_DATE_cache + etree.tostring(zz, pretty_print=True)
                            BRAN_DATE = BRAN_DATE_cache
                            BRAN_DATE = re.sub('<[^<]+?>', '', BRAN_DATE)
                            BRAN_DATE = BRAN_DATE.strip()
                            BRAN_DATE = re.sub('\n+', '', BRAN_DATE)
                        else :
                            BRAN_DATE = 'noDate'

                        BRAN_DATE = time.mktime(datetime.datetime.strptime(BRAN_DATE,'%B %d, %Y').timetuple())

                    except Exception as e:
                        BRAN_DATE = '00000000'

                    if len(RAW_BRAN) == 0:
                        RAW_BRAN = doc.xpath('//*[@id="brand"]/@href')
                        RAW_BRAN = RAW_BRAN[0].split("/",2)
                        RAW_BRAN[0] = RAW_BRAN[1]

                    if len(RAW_PRICE) == 0:
                        RAW_PRICE = ['no']
                    print '====GOOD====',RAW_BRAN,url
                    data = {
                        'ASIN': i,
                        'NAME': RAW_NAME,
                        'BRAN': RAW_BRAN[0],
                        'PRICE': RAW_PRICE[0],
                        'DEC':RAW_DEC,
                        'IMG':RAW_IMG[0],
                        'DATE': BRAN_DATE,
                        'DATE_CRATED': int(time.mktime(time.localtime()))
                    }
                    dataFromAsin.insert_one(data)
                    rankForAsin.insert_one({
                        'ASIN':i,
                        'RANKs':[{
                            'time':int(time.mktime(time.localtime())),
                            'RANK':RAW_RANK
                        }]
                    })
                else:
                    print '==========SORRY=============',url,proxy
                    errorAsin.insert_one({
                        'ASIN':i,
                        'proxy':proxy
                    })

            except Exception as e:
                print 'xx', e, url

                return reGetTitle(i)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return  reGetTitle(i)

if __name__ == "__main__":
    iz = 1
    result = list(dataAsin.find({}))
    print 'len(result)',len(result)
    AsinList = np.array_split(result, iz)
    threads = []
    try:
        for n in range(0, iz):
            name ='t'+ str(n)
            threads.append(threading.Thread(name=name,target=ReadAsin, args=(AsinList[n],)))
            threads[-1].start()  # start the thread we just created
        for t in threads:
            print t
            t.join()
        print 'DONE !'
    except requests.exceptions.RequestException as e:
        print ("error",e)




