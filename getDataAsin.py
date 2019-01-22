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
this = sys.modules[__name__] # this is now your current namespace
extracted_data = []
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
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.1241.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2241.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.3241.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.4241.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.5241.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.6241.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.7241.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.8241.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9241.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9141.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9341.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9441.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9541.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9641.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9741.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9841.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9941.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9911.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9921.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9931.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9961.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9951.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9971.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9981.90 Safari/537.36'},{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9991.90 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9992.91 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9993.92 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9994.93 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9995.94 Safari/537.36'},
{
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.9996.95 Safari/537.36'},

    ]


def ReadAsin(dataAsins):
    tim = 0
    headers = random.choice(headers_list)
    for listAsin in dataAsins:
        x = listAsin['dataAsin']
        for i in x :
            url = "http://www.amazon.com/dp/" + i
            try:
                page = requests.get(url,headers=headers, timeout=123)
                try:
                    doc = html.fromstring(page.content)

                    XPATH_NAME = '//*[@id="detailBullets_feature_div"]/ul/li[1]/span/span[1]/text()'
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
                    data = {
                        'NAME': RAW_NAME,
                        'head': headers,
                        'URL': url,
                        'ASIN': i
                    }
                    extracted_data.append(data)
                    # for article in RAW_NAME:
                    print '===done===', tim, i ,RAW_NAME
                    tim += 1
                except Exception as e:
                    print 'xx',e,i
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print 'yy',e




if __name__ == "__main__":
    result = json.load(urllib.urlopen('data.json'))
    AsinList = np.array_split(result, 5)
    try:
        t1 = threading.Thread(name='t1',target=ReadAsin, args=(AsinList[0],))
        t2 = threading.Thread(name='t2',target=ReadAsin, args=(AsinList[1],))
        t3 = threading.Thread(name='t3',target=ReadAsin, args=(AsinList[2],))
        t4 = threading.Thread(name='t4',target=ReadAsin, args=(AsinList[3],))
        t5 = threading.Thread(name='t5',target=ReadAsin, args=(AsinList[4],))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

        f = open('dataTest.json', 'w')
        json.dump(extracted_data, f, indent=4)
        f.close()
        print 'DONE !'
    except:
        print ("error")




