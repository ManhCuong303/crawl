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

json_data = open('Chrome-user-agents.json').read()
headers_list = json.loads(json_data)
ip_data = open('ip_list.json').read()
ip_list = json.loads(ip_data)


def ReadAsin(dataAsins):
    tim = 0
    headers = random.choice(headers_list)
    proxy = random.choice(ip_list)
    for listAsin in dataAsins:
        x = listAsin['dataAsin']
        for i in x :
            url = "http://www.amazon.com/dp/" + i
            try:
                page = requests.get(url, headers=headers, proxies=proxy, timeout=30)
                try:
                    doc = html.fromstring(page.content)

                    XPATH_NAME = '//*[@id="detailBullets_feature_div"]/ul/li'
                    # XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
                    # XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
                    # XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
                    # XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
                    #
                    RAW_NAME = doc.xpath(XPATH_NAME)
                    # RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
                    # RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
                    # RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
                    # RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
                    #
                    # NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
                    # SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
                    # CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
                    # ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
                    # AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
                    #
                    # if not ORIGINAL_PRICE:
                    #     ORIGINAL_PRICE = SALE_PRICE

                    if page.status_code != 200:
                        print 'URL', url
                        raise ValueError('captha')
                    RAW_NAME_cache =''
                    for article in RAW_NAME:
                        RAW_NAME_cache = RAW_NAME_cache + etree.tostring(article, pretty_print=True)

                    RAW_NAME = re.sub('<[^<]+?>', '', RAW_NAME_cache)

                    RAW_NAME = RAW_NAME.replace(" ", "")

                    RAW_NAME = re.sub('\n+',',',RAW_NAME)


                    data = {
                        'NAME': RAW_NAME,
                        'head': headers,
                        'URL': url,
                        'ASIN': i
                    }
                    extracted_data.append(data)
                    # for article in RAW_NAME:
                    print '===done===',i,RAW_NAME
                    tim += 1
                except Exception as e:
                    print 'xx',e,i
                    kap = {
                        'head': headers,
                        'proxy': proxy,
                        'url': url,
                        'status': e,
                    }
                    fail_getByAsin.append(kap)

            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print 'yy',headers,url,proxy,e
                kap = {
                    'proxy': proxy,
                    'url': url,
                    'status': "Cannot connect to proxy.",
                }
                fail_getByAsin.append(kap)




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

        f = open('fail_getByAsin.json', 'w')
        json.dump(fail_getByAsin, f, indent=4)
        f.close()


        print 'DONE !'
    except requests.exceptions.RequestException as e:
        print ("error",e)




