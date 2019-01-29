from lxml import html, etree
import csv, os, json
import random
import requests
import json
from exceptions import ValueError
from time import sleep
from threading import Thread
import threading
import numpy as np



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
                    print 'zzzz',url
                    print '=======GOOD======',RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                    return RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4

            except Exception as e:
                print 'not xpath', proxy, headers, e
                return getAsin(url)
        else:
            print 'errer', url, headers
            return getAsin(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
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
        Asin_data.append(getAsin(urlShare))

def buidUrl(url,count):
    iz = 50
    headers = random.choice(headers_list)
    proxy = random.choice(ip_list)

    try:
        page = requests.get(url, headers=headers, proxies=proxy, timeout=60)
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
        iz = 2
        x = np.arange(RAW_NUMPAGE)
        num = np.array_split(x, iz)

    except Exception as e:  # This is the correct syntax
        print 'not page 2222', '--', proxy, headers, e
        return buidUrl(url, count)

    print num[0] ,'-------',iz

    try:
        for n in xrange(0, 1):
            name = 't' + str(n) + 'v' + str(count)
            threads.append(threading.Thread(name=name, target=urlPage, args=(num[0],url,)))
            threads[-1].start()  # start the thread we just created
        for t in threads:
            t.join()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print 'error', e, '--', proxy, '--', headers

if __name__ == "__main__":

    urls = [
        'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624%2Cp_n_feature_browse-bin%3A368722011',
    ]
    for i in xrange(0,len(urls)):
        count = i
        buidUrl(urls[i],count)

    f = open('data.json', 'w')
    # Asin_data = list(set(Asin_data))
    json.dump(Asin_data, f, indent=4)
    f.close()

    f = open('fail-data.json', 'w')
    json.dump(fail_data, f, indent=4)
    f.close()

    print 'DONE !'
