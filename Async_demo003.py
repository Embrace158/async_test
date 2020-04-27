#__author:Administrator  
#data:2020/4/26
import asyncio
import csv
import os
import random
import json
import time

import aiohttp
t1=time.time()

async def fetch(session, url):
    user_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    ]
    header={'User-Agent':random.choice(user_agent)}
    async with session.get(url=url,headers=header) as response:
        return await response.text()

async def parse(html):
    ids=json.loads(html)['data']['areaTree']
    for id_item in ids:
        url='https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode='+id_item['id']
        country=id_item['name']
        await parse2(url,country)

async def parse2(url,name):
    async with aiohttp.ClientSession() as session:
        htmls = await fetch(session, url)
        infoMas = json.loads(htmls)['data']['list']
        # print(infoMas)
        for info_item in infoMas:
            country=name
            date=info_item['date']
            #当天数据
            today=info_item['today']
            confirm=today['confirm']
            suspect=today['suspect']
            heal=today['heal']
            dead=today['dead']
            severe=today['severe']
            #总计
            total=info_item['total']
            total_confirm = total['confirm']
            total_suspect = total['suspect']
            total_heal = total['heal']
            total_dead = total['dead']
            total_severe = total['severe']
            item=(country,date,confirm,suspect,heal,dead,severe,total_confirm,total_suspect,total_heal,total_dead,total_severe)
            print(item)
            await write(item)

async def write(item):
    if os.path.exists('COVID-19.csv'):
        f = open('COVID-19.csv', mode='a', encoding='utf-8-sig', newline='')
        w = csv.writer(f)
        w.writerow(item)
    else:
        f = open('COVID-19.csv', mode='a', encoding='utf-8-sig', newline='')
        w = csv.writer(f)
        w.writerow(['国家', '日期', '当天新增确诊', '当天新增疑似', '当天新增治愈', '当天新增死亡','当天新增重症','确诊', '疑似', '治愈', '死亡','重症'])
        w.writerow(item)


async def download(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        await parse(html)


if __name__ == '__main__':
    start_url='https://c.m.163.com/ug/api/wuhan/app/data/list-total'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download(start_url))
    t2 = time.time()
    print(t2-t1)