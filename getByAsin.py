from lxml import html, etree
import csv, os, json
import random
import requests
import json
from exceptions import ValueError
from time import sleep
from threading import Thread
import threading

headers_list = [
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2211.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2111.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.3211.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2221.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2212.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2213.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2214.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2215.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2216.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2217.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2218.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2219.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2231.90 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2241.90 Safari/537.36'},
    ]
Asin_data = []
def getAsin(url):
    headers = random.choice(headers_list)
    try:
        page = requests.get(url, headers=headers)
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
                        print 'xxxxxxxxx', RAW_ASIN
                        RAW_ASIN = doc.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/@data-asin')
                        print 'zzzzzzzzzzzz', RAW_ASIN
                    # NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
                    # SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
                    # CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
                    # ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
                    # AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
                    print 'dataAsin', len(RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4)
                    if len(RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4) == 0:
                        print 'headers',headers,'------------',url
                    return {
                        'dataAsin': RAW_ASIN + RAW_ASIN2 + RAW_ASIN3 + RAW_ASIN4
                    }

                except Exception as e:
                    print e
        else:
            print 'errer', url, headers
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print e

def urlPage(num):
    url = 'https://www.amazon.com/s?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&page=1&qid=1547780533&ref=lp_1045624_pg_1'
    headers = random.choice(headers_list)
    page = requests.get(url, headers=headers)
    doc = html.fromstring(page.content)
    XPATH_NUMPAGE = '//*[@id="pagn"]/span[6]/text()'
    RAW_NUMPAGE = doc.xpath(XPATH_NUMPAGE)
    # for article in RAW_NUMPAGE:
        # print 'aaaaaaaaa',etree.tostring(article, pretty_print=True)
    RAW_NUMPAGE = int(float(RAW_NUMPAGE[0]))
    if num == 'chan':
        for i in xrange(2, RAW_NUMPAGE + 1,2):
            urlShare = 'https://www.amazon.com/s?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&page=' + str(
                i) + '&qid=1547780533&ref=lp_1045624_pg_' + str(i)
            sleep(2)
            Asin_data.append(getAsin(urlShare))
            print  'done chan: ', i, '----', urlShare
    else:
        for i in xrange(1,RAW_NUMPAGE + 1,2):
            urlShare = 'https://www.amazon.com/s?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&page=' + str(
                i) + '&qid=1547780533&ref=lp_1045624_pg_' + str(i)
            sleep(2)
            Asin_data.append(getAsin(urlShare))
            print  'done le: ', i, '----', urlShare


if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=urlPage, args=('chan',))
        t2 = threading.Thread(target=urlPage, args=('le',))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        f = open('dataTest.json', 'w')
        json.dump(Asin_data, f, indent=4)
        f.close()
        print 'DONE !'
    except:
        print ("error")


