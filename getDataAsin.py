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

this = sys.modules[__name__] # this is now your current namespace
extracted_data = []
fail_getByAsin = []
textC = 'ShippingWeight:,4.8'

json_data = open('Chrome-user-agents.json').read()
headers_list = json.loads(json_data)
ip_data = open('ip_list.json').read()
ip_list = json.loads(ip_data)


def ReadAsin(dataAsins):

    headers = random.choice(headers_list)
    proxy = random.choice(ip_list)
    for listAsin in dataAsins:
        x = listAsin['dataAsin']
        for i in x :
            reGetTitle(i)


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

            if RAW_CHECK.find('ShippingWeight') != -1:
                XPATH_PRICE = '//*[@id="priceblock_ourprice"]/text()'
                XPATH_BRAN = '//*[@id="bylineInfo"]/text()'
                XPATH_NAME = '//h1[@id="title"]//text()'
                XPATH_PRICE = '//*[@id="priceblock_ourprice"]'
                XPATH_RANK = '//*[@id="SalesRank"]/text()'

                RAW_PRICE = doc.xpath(XPATH_PRICE)
                RAW_NAME = doc.xpath(XPATH_NAME)
                RAW_NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
                RAW_RANK = doc.xpath(XPATH_RANK)
                RAW_RANK = RAW_RANK[1].split()
                RAW_RANK = RAW_RANK[0]
                RAW_BRAN = doc.xpath(XPATH_BRAN)

                if len(RAW_PRICE) == 0:
                    RAW_PRICE = 'no'

                data = {
                    'ASIN': i,
                    'NAME': RAW_NAME,
                    'RANK': RAW_RANK,
                    'BRAN': RAW_BRAN,
                    'PRICE': RAW_PRICE[0]
                }

                print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',data

                extracted_data.append(data)
            # for article in RAW_CHECK:
            print '===done===',i

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

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return  reGetTitle(i)

if __name__ == "__main__":
    result = json.load(urllib.urlopen('dataTest.json'))
    AsinList = np.array_split(result, 10)
    try:
        t1 = threading.Thread(name='t1',target=ReadAsin, args=(AsinList[0],))
        t2 = threading.Thread(name='t2',target=ReadAsin, args=(AsinList[1],))
        t3 = threading.Thread(name='t3',target=ReadAsin, args=(AsinList[2],))
        t4 = threading.Thread(name='t4',target=ReadAsin, args=(AsinList[3],))
        t5 = threading.Thread(name='t5',target=ReadAsin, args=(AsinList[4],))
        t6 = threading.Thread(name='t5', target=ReadAsin, args=(AsinList[5],))
        t7 = threading.Thread(name='t5', target=ReadAsin, args=(AsinList[6],))
        t8 = threading.Thread(name='t5', target=ReadAsin, args=(AsinList[7],))
        t9 = threading.Thread(name='t5', target=ReadAsin, args=(AsinList[8],))
        t10 = threading.Thread(name='t5', target=ReadAsin, args=(AsinList[9],))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
        t9.start()
        t10.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        t10.join()

        f = open('dataAsin.json', 'w')
        json.dump(extracted_data, f, indent=4)
        f.close()



        print 'DONE !'
    except requests.exceptions.RequestException as e:
        print ("error",e)




