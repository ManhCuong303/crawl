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
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.dataAsin
coll = db['listAsinCache']
coll2 = db['listAsinReal']
threads = []
json_data = open('Chrome-user-agents.json').read()
headers_list = json.loads(json_data)
ip_data = open('ip_list.json').read()
ip_list = json.loads(ip_data)
Asin_data = []
fail_data = []



def getAsin(url):
    headers = random.choice(headers_list)
    proxy = random.choice(ip_list)
    try:
        page = requests.get(url, headers=headers, proxies=proxy, timeout=60)
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

                if len(RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4) == 0:
                    RAW_ASIN = doc.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/@data-asin')
                    if len(RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4) == 0:
                        print '=======FAIL=======',headers,proxy,RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                        kap = {
                            'headers': headers,
                            'proxy': proxy,
                            'url': url,
                            'status': "dataAsin = 0, capcha",
                        }
                        fail_data.append(kap)
                        return getAsin(url)

                else:
                    print '=======GOOD======',RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                    zt = RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                    for kaak in zt:
                        check_ASIN = '//*[@data-asin="' + str(kaak) + '"]'
                        fid = {'ASIN': kaak}
                        showcoll = coll.count_documents(fid)
                        CHECK_RAW = doc.xpath(check_ASIN)

                        CHECK_RAW_cache = ''
                        for rawdec in CHECK_RAW:
                            CHECK_RAW_cache = CHECK_RAW_cache + etree.tostring(rawdec, pretty_print=True)

                        if CHECK_RAW_cache.find(
                                'https://images-na.ssl-images-amazon.com/images/I/41coxNoci9L._AC_UL260_SR200,260_.jpg') != -1:
                            coll2.insert_one(fid)
                            if showcoll == 0:
                                coll.insert_one(fid)
                        if CHECK_RAW_cache.find(
                                'https://images-na.ssl-images-amazon.com/images/I/41B7dj8jHtL._AC_UL260_SR200,260_.jpg') != -1:
                            coll2.insert_one(fid)
                            if showcoll == 0:
                                coll.insert_one(fid)

                    return RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4

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

def buidUrl(url,count):
    iz = 50
    headers = random.choice(headers_list)
    proxy = random.choice(ip_list)

    try:
        page = requests.get(url, headers=headers, proxies=proxy, timeout=60)
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

            RAW_NUMPAGE = int(float(RAW_NUMPAGE[0]))

            if 10 < RAW_NUMPAGE < 50 :
                iz = 10
            elif RAW_NUMPAGE < 10 :
                iz = RAW_NUMPAGE
            else:
                iz = 50

            x = np.arange(RAW_NUMPAGE)
            num = np.array_split(x, iz)
        else:
            print 'page.status_code',page.status_code, url, headers
            buidUrl(url, count)

    except Exception as e:  # This is the correct syntax
        print 'not page 2222', '--', proxy, headers, e,url
        buidUrl(url, count)

    try:
        for n in xrange(0, iz):
            name = 't' + str(n) + 'v' + str(count)
            threads.append(threading.Thread(name=name, target=urlPage, args=(num[n],url,)))
            threads[-1].start()  # start the thread we just created
        for t in threads:
            t.join()

    except Exception as e:  # This is the correct syntax
        print 'error', e, '--', proxy, '--', headers

if __name__ == "__main__":

    urls = [
        'https://www.amazon.com/s/ref=sr_pg_2?fst=p90x%3A1&rh=n%3A7141123011%2Cn%3A7147445011%2Cn%3A12035955011%2Cn%3A9103696011%2Cn%3A9056985011%2Cn%3A9056986011%2Cn%3A9056987011%2Ck%3At+shirt+dad+and+son&keywords=t+shirt+dad+and+son',
        'https://www.amazon.com/s/ref=sr_pg_3?fst=p90x%3A1&rh=n%3A7141123011%2Cn%3A7147445011%2Cn%3A12035955011%2Cn%3A9103696011%2Cn%3A9056985011%2Cn%3A9056986011%2Cn%3A9056987011%2Ck%3At+shirt+dad+and+son&sort=price-asc-rank&keywords=t+shirt+dad+and+son',
        'https://www.amazon.com/s/ref=sr_pg_3?fst=p90x%3A1&rh=n%3A7141123011%2Cn%3A7147445011%2Cn%3A12035955011%2Cn%3A9103696011%2Cn%3A9056985011%2Cn%3A9056986011%2Cn%3A9056987011%2Ck%3At+shirt+dad+and+son&sort=price-desc-rank&keywords=t+shirt+dad+and+son',
        'https://www.amazon.com/s/ref=sr_pg_3?fst=p90x%3A1&rh=n%3A7141123011%2Cn%3A7147445011%2Cn%3A12035955011%2Cn%3A9103696011%2Cn%3A9056985011%2Cn%3A9056986011%2Cn%3A9056987011%2Ck%3At+shirt+dad+and+son&sort=review-rank&keywords=t+shirt+dad+and+son',
        'https://www.amazon.com/s/ref=sr_pg_2?fst=p90x%3A1&rh=n%3A7141123011%2Cn%3A7147445011%2Cn%3A12035955011%2Cn%3A9103696011%2Cn%3A9056985011%2Cn%3A9056986011%2Cn%3A9056987011%2Ck%3At+shirt+dad+and+son&sort=date-desc-rank&keywords=t+shirt+dad+and+son',
    ]
    for i in xrange(0,len(urls)):
        count = i
        buidUrl(urls[i],count)



    # f = open('fail-data.json', 'w')
    # json.dump(fail_data, f, indent=4)
    # f.close()

    print 'DONE !'