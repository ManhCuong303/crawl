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
        page = requests.get(url, headers=headers, proxies=proxy,timeout=60)
        print page.status_code
        if page.status_code == 200:
            while True:
                sleep(2)
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

                    # NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
                    # SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
                    # CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
                    # ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
                    # AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
                    print 'dataAsin', len(RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4)
                    if len(RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4) == 0:
                        print 'headers',headers,proxy,'------------',url
                        fail_data.append({
                            'headers': headers,
                            'proxy': proxy,
                            'url': url,
                            'status': 'dataAsin = 0, capcha',
                        })
                        print fail_data
                    return {
                        'dataAsin': RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                    }

                except Exception as e:
                    print 'not xpath',proxy,headers,e
                    fail_data.append({
                        'headers': headers,
                        'proxy': proxy,
                        'url': url,
                        'status': e

                    })
        else:
            print 'errer', url, headers
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print 'not page', '--', proxy, headers, e
        fail_data.append({
            'headers':headers,
            'proxy':proxy,
            'url':url,
            'status': e
        })

def urlPage(num):
    for i in num:
        urlShare = 'https://www.amazon.com/s?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&page=' + str(
            i) + '&qid=1547780533&ref=lp_1045624_pg_' + str(i)
        sleep(2)
        Asin_data.append(getAsin(urlShare))

if __name__ == "__main__":

    url = 'https://www.amazon.com/s?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&page=1&qid=1547780533&ref=lp_1045624_pg_1'

    headers = random.choice(headers_list)
    proxy = random.choice(ip_list)
    print headers
    page = requests.get(url, headers=headers,proxies=proxy,timeout=60)
    doc = html.fromstring(page.content)
    XPATH_NUMPAGE = '//*[@id="pagn"]/span[6]/text()'
    RAW_NUMPAGE = doc.xpath(XPATH_NUMPAGE)
    RAW_NUMPAGE = int(float(RAW_NUMPAGE[0]))
    x = np.arange(RAW_NUMPAGE)
    num = np.split(x,10)
    try:
        t1 = threading.Thread(target=urlPage, args=(num[0],))
        t2 = threading.Thread(target=urlPage, args=(num[1],))
        t3 = threading.Thread(target=urlPage, args=(num[2],))
        t4 = threading.Thread(target=urlPage, args=(num[3],))
        t5 = threading.Thread(target=urlPage, args=(num[4],))
        t6 = threading.Thread(target=urlPage, args=(num[5],))
        t7 = threading.Thread(target=urlPage, args=(num[6],))
        t8 = threading.Thread(target=urlPage, args=(num[7],))
        t9 = threading.Thread(target=urlPage, args=(num[8],))
        t10 = threading.Thread(target=urlPage, args=(num[9],))

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

        f = open('data.json', 'w')
        json.dump(Asin_data, f, indent=4)
        f.close()

        f = open('fail-data.json', 'w')
        json.dump(fail_data, f, indent=4)
        f.close()
        print 'DONE !'
    except:
        print ("error")


