from lxml import html, etree
import csv, os, json
import random
import requests
import json
import re
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
listIPUS = list(ip_list.find({'geted':'false'}))
AllAsin = db['AllAsin']
iplist = db['iplist']
listIPAll = list(iplist.find({'geted':'false'}))
Asin_data = []
fail_data = []
textFind = 'ShippingWeight:,4.8'


def getAsin(url):
    countIplist = ip_list.count({'geted': 'false'})
    if countIplist > 0:
        try:
            randomProxy = random.choice(listIPUS)
            idRandom = randomProxy['id']
            timeNow = int(time.mktime(time.localtime()))
            if timeNow - randomProxy['dateGet'] >= 30:

                headers = random.choice(headers_list)
                proxy = randomProxy['data']

                if proxy[1]['status'] + 1 >= 5:
                    ip_list.update({'id': idRandom}, {'$set': {"geted": 'true'}})
                    if listIPUS.index(randomProxy):
                        listIPUS.remove(randomProxy)
                    buidUrl(url, count)
                else:
                    try:
                        page = requests.get(url, headers=headers, proxies=proxy[0], timeout=60)
                        randomProxy['dateGet'] = int(time.mktime(time.localtime()))
                        ip_list.update({'id': idRandom}, randomProxy)
                        if listIPUS.index(randomProxy):
                            listIPUS[listIPUS.index(randomProxy)] = randomProxy

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
                                RAW_ASIN5 = doc.xpath(
                                    '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/@data-asin')

                                zt = RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4 + RAW_ASIN5

                                if len(zt) == 0:
                                    print '=======FAIL=======', headers, proxy, RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                                    proxy[1]['status'] = proxy[1]['status'] + 1
                                    randomProxy['data'] = proxy
                                    randomProxy['dateGet'] = int(time.mktime(time.localtime()))
                                    ip_list.update({'id': idRandom}, randomProxy)
                                    if listIPUS.index(randomProxy):
                                        listIPUS[listIPUS.index(randomProxy)] = randomProxy
                                    return 'FAIL'
                                elif len(zt) != 0 and len(RAW_ASIN5) == 0:
                                    for kaak in zt:
                                        check_ASIN = '//*[@data-asin="' + str(kaak) + '"]'
                                        fid = {'ASIN': kaak}
                                        showcoll = coll.count_documents(fid)
                                        CHECK_RAW = doc.xpath(check_ASIN)

                                        CHECK_RAW_cache = ''

                                        for rawdec in CHECK_RAW:
                                            CHECK_RAW_cache = CHECK_RAW_cache + etree.tostring(rawdec,
                                                                                               pretty_print=True)

                                        fid = {'ASIN': kaak, 'geted': 'false',
                                               'date': int(time.mktime(time.localtime())),
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
                                        fid = {'ASIN': kaak, 'geted': 'false',
                                               'date': int(time.mktime(time.localtime())),
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

                        proxy[1]['status'] = proxy[1]['status'] + 1
                        randomProxy['data'] = proxy
                        randomProxy['dateGet'] = int(time.mktime(time.localtime()))
                        ip_list.update({'id': idRandom}, randomProxy)
                        if listIPUS.index(randomProxy):
                            listIPUS[listIPUS.index(randomProxy)] = randomProxy
                        print e, proxy
                        return getAsin(url)

            else:
                print '====reGet proxy page 400====='
                getAsin(url)
        except Exception as e:  # This is the correct syntax
            print 'not page', '--', proxy, headers, e, url
            sleep(10)
            getAsin(url)
    else:
        sleep(10)
        print 'not proxy page'
        return 'not proxy page'

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

def geturl2(dataAsins):
    for listAsin in dataAsins:
        i = listAsin['ASIN']
        getAsinPart2(i)
    print 'DONE K'


def getAsinPart2(i):
    url = "https://www.amazon.com/dp/" + i
    countIplist = iplist.count({'geted':'false'})
    if countIplist > 100:
        try:
            randomProxy = random.choice(listIPAll)
            idRandom = randomProxy['id']
            timeNow = int(time.mktime(time.localtime()))
            if  timeNow - randomProxy['dateGet'] >= 30:
                headers = random.choice(headers_list)
                proxy = randomProxy['data']
                proxyAdd = proxy
                if proxy[1]['status'] + 1 >= 5:
                    randomProxy['geted'] = 'true'
                    iplist.update({'id': idRandom}, randomProxy)
                    if listIPAll.index(randomProxy):
                        listIPAll.remove(randomProxy)
                    getAsinPart2(i)
                else:
                    try:
                        page = requests.get(url, headers=headers, proxies=proxy[0], timeout=60)

                        randomProxy['dateGet'] = int(time.mktime(time.localtime()))
                        iplist.update({'id': idRandom}, {'$set': {"data": proxy}})
                        if listIPAll.index(randomProxy):
                            listIPAll[listIPAll.index(randomProxy)] = randomProxy

                        if page.status_code == 200:
                            try:

                                doc = html.fromstring(page.content)

                                XPATH_CHECK = '//*[@id="detailBullets_feature_div"]'

                                RAW_CHECK = doc.xpath(XPATH_CHECK)

                                RAW_CHECK_cache = ''

                                if len(RAW_CHECK) == 0:
                                    RAW_CHECK = doc.xpath('//*[@id="detail-bullets"]')
                                for article in RAW_CHECK:
                                    RAW_CHECK_cache = RAW_CHECK_cache + etree.tostring(article, pretty_print=True)

                                RAW_CHECK = re.sub('<[^<]+?>', '', RAW_CHECK_cache)
                                RAW_CHECK = RAW_CHECK.replace(" ", "")
                                RAW_CHECK = re.sub('\n+', ',', RAW_CHECK)

                                if RAW_CHECK.find(textFind) != -1:
                                    fid = {'ASIN': i, 'geted': 'false', 'date': int(time.mktime(time.localtime())),
                                           'status': 'true'}
                                    fidx = {'ASIN': i}
                                    showcoll2 = coll.count_documents(fidx)
                                    if showcoll2 == 0:
                                        coll.insert_one(fid)
                                        print '=======GOOD======='
                                        AllAsin.remove({'ASIN': i})
                                    else:
                                        AllAsin.remove({'ASIN': i})
                                        print '===========2 ASIN==========='
                                else:
                                    print '========NOT 4.8=========='
                                    AllAsin.remove({'ASIN': i})
                            except Exception as e:
                                print 'xxxx', e, url
                                getAsinPart2(i)
                        else:
                            print '--------Page die !-----------'
                            AllAsin.update({'ASIN': i}, {'$set': {"status": 'false'}})
                            AllAsin.update({'ASIN': i}, {'$set': {"geted": 'true'}})

                            return i
                    except Exception as e:  # This is the correct syntax
                        print e
                        proxy[1]['status'] = proxy[1]['status'] + 1
                        randomProxy['data'] = proxy
                        randomProxy['dateGet'] =  int(time.mktime(time.localtime()))
                        iplist.update({'id': idRandom}, {'$set': {"data": proxy}})
                        if listIPAll.index(randomProxy) :
                            listIPAll[listIPAll.index(randomProxy)] = randomProxy
                        getAsinPart2(i)
            else:
                print '====reGet proxy====='
                getAsinPart2(i)
        except Exception as e:
            print 'error random ',e
            getAsinPart2(i)
    else:
        print 'not proxy'
        return 'not proxy'



def buidUrl(url,count):
    countIplist = ip_list.count({'geted':'false'})
    if countIplist > 0:
        iz = 1
        try:
            randomProxy = random.choice(listIPUS)
            idRandom = randomProxy['id']
            timeNow = int(time.mktime(time.localtime()))

            if timeNow - randomProxy['dateGet'] >= 30:
                headers = random.choice(headers_list)
                proxy = randomProxy['data']
                if proxy[1]['status'] + 1 >= 5:
                    ip_list.update({'id': idRandom}, {'$set': {"geted": 'true'}})
                    if listIPUS.index(randomProxy):
                        listIPUS.remove(randomProxy)
                    buidUrl(url, count)
                else:
                    try:
                        page = requests.get(url, proxies=proxy[0],headers=headers, timeout=60)

                        randomProxy['dateGet'] = int(time.mktime(time.localtime()))
                        ip_list.update({'id': idRandom},randomProxy)
                        if listIPUS.index(randomProxy):
                            listIPUS[listIPUS.index(randomProxy)] = randomProxy

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
                            try:
                                RAW_NUMPAGE = int(float(RAW_NUMPAGE[0]))
                            except Exception as e:
                                RAW_NUMPAGE = int(float(RAW_NUMPAGE[3]))

                            if 10 < RAW_NUMPAGE < 50 :
                                iz = 10
                            elif RAW_NUMPAGE < 10 :
                                iz = RAW_NUMPAGE
                            else:
                                iz =200
                            iz = 50
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
                        print e
                        proxy[1]['status'] = proxy[1]['status'] + 1
                        randomProxy['data'] = proxy
                        randomProxy['dateGet'] = int(time.mktime(time.localtime()))
                        ip_list.update({'id': idRandom}, randomProxy)
                        if listIPUS.index(randomProxy):
                            listIPUS[listIPUS.index(randomProxy)] = randomProxy
                        buidUrl(url, count)

            else:
                print '====reGet proxy page 400====='
                sleep(10)
                buidUrl(url, count)
        except Exception as e:  # This is the correct syntax
            print 'not page 400'
            buidUrl(url, count)
    else:
        print 'not proxy page 400'
        return 'not proxy page 400'

if __name__ == "__main__":

    urls = [
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=price-asc-rank&dc&qid=1550207257&ref=sr_pg_2',
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=relevancerank&dc&qid=1550207306&ref=sr_pg_2',
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=price-desc-rank&dc&qid=1550207351&ref=sr_pg_2',
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=review-rank&dc&qid=1550207376&ref=sr_pg_2',
        'https://www.amazon.com/s?k=t-shirts+dad+and+son&i=fashion&s=date-desc-rank&dc&qid=1550207404&ref=sr_pg_2',

        'https://www.amazon.com/s?k=t+shirt+dad+and&i=fashion-novelty&bbn=12035955011&rh=p_6%3AATVPDKIKX0DER&hidden-keywords=ORCA&ref=amb_link_483004722_1',
        'https://www.amazon.com/s?k=t+shirt+dad+and&i=fashion-novelty&bbn=12035955011&rh=p_6%3AATVPDKIKX0DER&s=price-asc-rank&hidden-keywords=ORCA&qid=1550456849&ref=sr_st_price-asc-rank',
        'https://www.amazon.com/s?k=t+shirt+dad+and&i=fashion-novelty&bbn=12035955011&rh=p_6%3AATVPDKIKX0DER&s=price-desc-rank&hidden-keywords=ORCA&qid=1550456883&ref=sr_st_price-desc-rank',
        'https://www.amazon.com/s?k=t+shirt+dad+and&i=fashion-novelty&bbn=12035955011&rh=p_6%3AATVPDKIKX0DER&s=review-rank&hidden-keywords=ORCA&qid=1550456902&ref=sr_st_review-rank',
        'https://www.amazon.com/s?k=t+shirt+dad+and&i=fashion-novelty&bbn=12035955011&rh=p_6%3AATVPDKIKX0DER&s=date-desc-rank&hidden-keywords=ORCA&qid=1550456919&ref=sr_st_date-desc-rank',
    ]


    for i in xrange(0,len(urls)):
        count = i
        print 'zzzzzz', urls[i]
        buidUrl(urls[i],count)

    print 'DONE part 1!'

    sleep(2)

    print 'BEGIN part 2!'

    result = list(AllAsin.find({'geted':'false'}))

    print 'len(result)', len(result)
    if len(result) > 0:
        if 200 > len(result) > 10 :
            iz = 10
        elif len(result) <= 10:
            iz = 1
        else:
            iz = 200
        iz = 50
        AsinList = np.array_split(result, iz)
        threads = []
        try:
            for n in range(0, iz):
                name = 'k' + str(n)
                threads.append(threading.Thread(name=name, target=geturl2, args=(AsinList[n],)))
                threads[-1].start()  # start the thread we just created
            for t in threads:
                print t
                t.join()
            print 'DONE part 2'
        except requests.exceptions.RequestException as e:
            print ("error", e)
    else :
        print 'NO ASIN',


