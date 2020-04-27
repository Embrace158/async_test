#__author:Administrator  
#data:2020/4/25
import asyncio
import csv
import os
import random
import time

from lxml import etree
import aiohttp
import pandas as pd
import lxml
start_urls=['https://static1.scrape.cuiqingcai.com/page/{}'.format(i) for i in range(1,11)]
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
    if os.path.exists('dfcf/热门视频数据.csv'):
        f = open('dfcf/热门视频数据.csv', mode='a', encoding='utf-8-sig', newline='')
        w = csv.writer(f)
    else:
        f = open('dfcf/热门视频数据.csv', mode='a', encoding='utf-8-sig', newline='')
        w = csv.writer(f)
        w.writerow(['电影名', '电影得分', '电影链接', '电影时长', '电影上映日期', '标签'])
        # w.writerow(['标题', '视频简介', '分类', 'bv号', 'av号', '播放量', '弹幕数', '最高全站日排行', '点赞', "硬币", "收藏", "分享", 'up主', '标签'])
    area=[]
    videoDate=[]
    videoTime=[]
    hrefs=[]
    dynamics=[]
    html=lxml.etree.HTML(html.replace("\n",""))
    name=html.xpath(".//a[@class='name']/h2/text()")
    href=html.xpath(".//a[@class='name']/@href")
    for o in range(len(href)):
        hrefs.append('https://static1.scrape.cuiqingcai.com'+href[o])
    score=html.xpath(".//div[@class='el-col el-col-24 el-col-xs-5 el-col-sm-5 el-col-md-4']/p[1]/text()")
    collection=html.xpath(".//div[@class='m-v-sm info']/span/text()")
    for i in range(1,11):
        dynamic=html.xpath("//div[@class='el-card item m-t is-hover-shadow']"+str([i])+"/div/div/div[2]/div/button[@type='button']/span/text()")
        dynamics.append("".join(dynamic))
    for i in range(4,len(collection),4):
        area.append(collection[i-4])
        if len(collection[i-1])== 13:
            videoDate.append(collection[i-1])
        else:
            videoDate.append("null")
        videoTime.append(collection[i-2])
    videoDate.append(collection[len(collection)-1])
    videoTime.append(collection[len(collection)-2])
    Data=pd.DataFrame({'电影名':name,'电影得分':score,'电影链接':hrefs,'电影时长':videoTime,'电影上映日期':videoDate,'标签':dynamics})
    Data.to_csv('热门视频数据.csv', mode='a', header=False, index=False,sep=',' ,encoding='utf-8-sig')

async def download(url,sem):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        await parse(html)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    semaphore = asyncio.Semaphore(16)
    tasks = [asyncio.ensure_future(download(start_url,semaphore)) for start_url in start_urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)
    t2=time.time()
    print(t2-t1)