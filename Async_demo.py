#__author:Administrator
#data:2020/4/2
import asyncio
import csv
import datetime
import json
import os
import random
import time
import aiohttp
time_from=input("起始时间")
time_to=input("截止时间")
t1=time.time()
start_urls = ['https://s.search.bilibili.com/cate/search?search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id={}&page={}&pagesize=20&jsonp=jsonp&time_from={}&time_to={}'.format(c,i,time_from,time_to) for i in range(1,11) for c in range(17,31)]
# print(len(start_urls))
url2 = []

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
async def parse1(html1):
    json_data = json.loads(html1)
    json_data = json_data['result']
    for item in json_data:
        url2="https://api.bilibili.com/x/web-interface/view?&bvid=" + str(item['bvid'])
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url2)
            # print(html)
            await parse(html)
            # asyncio.sleep(1)



async def parse(html):
    if os.path.exists('{}-{}热门视频数据.csv'.format(time_from, time_to)):
        f = open('{}-{}热门视频数据.csv'.format(time_from, time_to), mode='a', encoding='utf-8-sig', newline='')
        w = csv.writer(f)
    else:
        f = open('{}-{}热门视频数据.csv'.format(time_from, time_to), mode='a', encoding='utf-8-sig', newline='')
        w = csv.writer(f)
        w.writerow(['标题', '视频简介', '分类', 'bv号', 'av号', '播放量', '弹幕数', '最高全站日排行', '点赞', "硬币", "收藏", "分享", 'up主', '标签'])
    json_data = json.loads(html)
    json_Info1 = json_data['data']
    bvidnum = json_Info1['bvid']
    aid = json_Info1['aid']
    tname = json_Info1['tname']
    title = json_Info1['title']
    desc = json_Info1['desc']
    own = json_Info1['owner']
    name = own['name']
    #             print(name)

    # #stat数据
    stat = json_Info1['stat']
    view = stat['view']
    danmu = stat['danmaku']
    reply = stat['reply']
    favorite = stat['favorite']
    coin = stat['coin']
    share = stat['share']
    like = stat['like']
    his_rank = stat['his_rank']
    dynamic = json_Info1['dynamic']
    value = (title, desc, tname,bvidnum, aid,view,danmu,his_rank,like, coin, favorite, share, name, dynamic)
    w.writerow(value)
    print(value)


async def download(url,sem):
    async with sem:
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)
            await parse1(html)
            time.sleep(0.2)
            
if __name__ == "__main__": 
    sem = asyncio.Semaphore(5)
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(download(start_url,sem)) for start_url in start_urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)
    t2=time.time()
    print(t2-t1)
