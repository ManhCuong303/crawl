from lxml import html, etree
import csv, os, json
import random
import requests
import json
from exceptions import ValueError
from time import sleep
from threading import Thread
import threading
from collections import OrderedDict
import numpy as np
import pymongo
import time
import datetime
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.dataAsin
coll = db['listAsinCache2']
coll2 = db['listAsinReal']
threads = []
json_data = open('Chrome-user-agents.json').read()
headers_list = json.loads(json_data)
ip_list  = db['ipUSList']
AllAsin = db['AllAsin']
Asin_data = []
fail_data = []


def getAsin(url):
    headers = random.choice(headers_list)
    countIplist = ip_list.count({})
    idRandom = random.randint(0, countIplist - 1)
    Getproxy = list(ip_list.find({'id': idRandom}))
    proxy = Getproxy[0]['data']
    proxyAdd = proxy
    try:
        page = requests.get(url, headers=headers, proxies=proxy[0], timeout=60)
        if page.status_code == 200:
            try:
                doc = html.fromstring(page.content)
                XPATH_ASIN = '//*[@id="mainResults"]/ul/li/@data-asin'
                XPATH_ASIN2 = '//*[@id="btfPreResults"]/ul/li/@data-asin'
                XPATH_ASIN3 = '//*[@id="atfResults"]/ul/li/@data-asin'
                XPATH_ASIN4 = '//*[@id="btfResults"]/ul/li/@data-asin'

                RAW_ASIN = doc.xpath(XPATH_ASIN)
                RAW_ASIN2 = doc.xpath(XPATH_ASIN2)
                RAW_ASIN3 = doc.xpath(XPATH_ASIN3)
                RAW_ASIN4 = doc.xpath(XPATH_ASIN4)
                RAW_ASIN5 = doc.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/@data-asin')

                zt = RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4 + RAW_ASIN5

                if len(zt) == 0:
                    print '=======FAIL=======',headers,proxy,RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                    return 'FAIL'
                elif len(zt) != 0 and len(RAW_ASIN5) == 0 :
                    for kaak in zt:
                        check_ASIN = '//*[@data-asin="' + str(kaak) + '"]'
                        fid = {'ASIN': kaak}
                        showcoll = coll.count_documents(fid)
                        CHECK_RAW = doc.xpath(check_ASIN)

                        CHECK_RAW_cache = ''
                        for rawdec in CHECK_RAW:
                            CHECK_RAW_cache = CHECK_RAW_cache + etree.tostring(rawdec, pretty_print=True)

                        fid = {'ASIN': kaak, 'geted': 'false', 'date': int(time.mktime(time.localtime())),
                               'status': 'true'}

                        if CHECK_RAW_cache.find(
                                'https://images-na.ssl-images-amazon.com/images/I/41coxNoci9L._AC_UL260_SR200,260_.jpg') != -1:

                            coll2.insert_one(fid)
                            if showcoll == 0:
                                print '=======GOOD======', RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                                coll.insert_one(fid)

                        if CHECK_RAW_cache.find(
                                'https://images-na.ssl-images-amazon.com/images/I/41B7dj8jHtL._AC_UL260_SR200,260_.jpg') != -1:
                            coll2.insert_one(fid)
                            if showcoll == 0:
                                print '=======GOOD======', RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                                coll.insert_one(fid)
                    return RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4 + RAW_ASIN5
                else:
                    for kaak in zt:
                        fid = {'ASIN': kaak}
                        showcoll = coll.count_documents(fid)
                        fid = {'ASIN': kaak, 'geted': 'false', 'date': int(time.mktime(time.localtime())),
                               'status': 'true'}
                        if showcoll == 0:
                            print '=======GOOD======', RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                            AllAsin.insert_one(fid)

            except Exception as e:
                print 'not xpath', proxy, headers, e
                return getAsin(url)
        else:
            print 'errer', url, headers
            return getAsin(url)
    except Exception as e:  # This is the correct syntax
        return getAsin(url)
    return 'no way'


def urlPage(num,url):
    sleep(2)
    for i in num:
        if i == 0 :
            continue
        urlShare = url + '&page=' + str(
            i)
        sleep(2)

        print urlShare

        getAsin(urlShare)

def test(num,url):
    return 'sss',num,url

def buidUrl(url,count):

    iz = 50
    headers = random.choice(headers_list)
    countIplist = ip_list.count({})
    idRandom = random.randint(0, countIplist)
    Getproxy = list(ip_list.find({'id': idRandom}))
    proxy = Getproxy[0]['data']
    proxyAdd = proxy

    try:
        print proxy[0]

        sleep(2)

        page = requests.get(url, proxies=proxy[0],headers=headers, timeout=60)
        if page.status_code == 200:
            doc = html.fromstring(page.content)
            XPATH_NUMPAGE = '//*[@id="pagn"]/span[6]/text()'
            RAW_NUMPAGE = doc.xpath(XPATH_NUMPAGE)
            if len(RAW_NUMPAGE) == 0:
                for ipz in xrange(1,6):
                    kaka = '//*[@id="pagn"]/span[' + str(6 - ipz) + ']/a/text()'
                    RAW_NUMPAGE = doc.xpath(kaka)
                    try:
                        if int(float(RAW_NUMPAGE[0])) :
                            break
                    except Exception as e:
                        continue
            if len(RAW_NUMPAGE) == 0 :
                RAW_NUMPAGE = doc.xpath('//li[@class="a-disabled"]/text()')

            RAW_NUMPAGE = int(float(RAW_NUMPAGE[0]))

            if 10 < RAW_NUMPAGE < 50 :
                iz = 10
            elif RAW_NUMPAGE < 10 :
                iz = RAW_NUMPAGE
            else:
                iz = 50
            iz = 10
            x = np.arange(RAW_NUMPAGE)
            num = np.array_split(x, iz)

            for n in xrange(0, iz):
                name = 't' + str(n) + 'v' + str(count)
                threads.append(threading.Thread(name=name, target=urlPage, args=(num[n], url,)))
                threads[-1].start()  # start the thread we just created
            for t in threads:
                t.join()

        else:
            print 'page.status_code',page.status_code, url, headers
            buidUrl(url, count)

    except Exception as e:  # This is the correct syntax
        print 'not page 2222', '--', proxy, headers, e,url
        buidUrl(url, count)


if __name__ == "__main__":

    urls = [
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=price-asc-rank&dc&qid=1550207257&ref=sr_pg_2',
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=relevancerank&dc&qid=1550207306&ref=sr_pg_2',
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=price-desc-rank&dc&qid=1550207351&ref=sr_pg_2',
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=review-rank&dc&qid=1550207376&ref=sr_pg_2',
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=date-desc-rank&dc&qid=1550207404&ref=sr_pg_2',

        # 'https://www.amazon.com/s?k=t+shirt+mom+and+son&i=fashion&s=price-asc-rank&dc&qid=1550207257&ref=sr_pg_2',
        # 'https://www.amazon.com/s?k=t+shirt+mom+and+son&i=fashion&s=relevancerank&dc&qid=1550207306&ref=sr_pg_2',
        # 'https://www.amazon.com/s?k=t+shirt+mom+and+son&i=fashion&s=price-desc-rank&dc&qid=1550207351&ref=sr_pg_2',
        # 'https://www.amazon.com/s?k=t+shirt+mom+and+son&i=fashion&s=review-rank&dc&qid=1550207376&ref=sr_pg_2',
        # 'https://www.amazon.com/s?k=t+shirt+mom+and+son&i=fashion&s=date-desc-rank&dc&qid=1550207404&ref=sr_pg_2',
    ]


    for i in xrange(0,len(urls)):
        count = i
        print 'zzzzzz', urls[i]
        buidUrl(urls[i],count)

    print 'DONE !'
