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
import multiprocessing.dummy as mp

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
        x = listAsin
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

            if RAW_CHECK.find(textC) != -1:
                XPATH_PRICE = '//*[@id="priceblock_ourprice"]/text()'
                XPATH_BRAN = '//*[@id="bylineInfo"]/text()'
                XPATH_NAME = '//h1[@id="title"]//text()'
                XPATH_RANK = '//*[@id="SalesRank"]/text()'

                RAW_PRICE = doc.xpath(XPATH_PRICE)
                RAW_NAME = doc.xpath(XPATH_NAME)
                RAW_NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
                RAW_RANK = doc.xpath(XPATH_RANK)
                RAW_RANK = RAW_RANK[1].split()
                RAW_RANK = RAW_RANK[0]
                RAW_BRAN = doc.xpath(XPATH_BRAN)

                if len(RAW_BRAN) == 0:
                    RAW_BRAN = doc.xpath('//*[@id="brand"]/@href')
                    RAW_BRAN = RAW_BRAN[0].split("/",2)
                    RAW_BRAN[0] = RAW_BRAN[1]

                if len(RAW_PRICE) == 0:
                    RAW_PRICE = ['no']
                print RAW_BRAN,'zzzzzzzz'
                data = {
                    'ASIN': i,
                    'NAME': RAW_NAME,
                    'RANK': RAW_RANK,
                    'BRAN': RAW_BRAN[0],
                    'PRICE': RAW_PRICE[0]
                }
                # print '===done===', i
                extracted_data.append(data)
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
        print "===Request=== ",len(count_asin_re)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return  reGetTitle(i)

if __name__ == "__main__":
    iz = 50
    result = json.load(urllib.urlopen('data.json'))
    AsinList = np.array_split(result, iz)
    threads = []
    try:
        for n in range(0, iz):
            name ='t'+ str(n)
            threads.append(threading.Thread(name=name,target=ReadAsin, args=(AsinList[n],)))
            threads[-1].start()  # start the thread we just created
        for t in threads:
            t.join()

        f = open('dataAsin.json', 'w')
        json.dump(extracted_data, f, indent=4)
        f.close()

        print 'DONE !'
    except requests.exceptions.RequestException as e:
        print ("error",e)




