import aiohttp
import json
import asyncio
import csv
import random
import os


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
    json_datas=json.loads(html)['data']
    for json_data in json_datas:
        stockCode=json_data['stockCode']#股票代码
        stockName=json_data['stockName']#股票名称
        title=json_data['title']#研报名称
        emRatingName=json_data['emRatingName']#原文评级
        sRatingName=json_data['sRatingName']#评级变动
        orgSName=json_data['orgSName']#机构
        count=json_data['count']#近一月个股研报数
        predictNextYearEps=json_data['predictNextYearEps']#2020盈利预测收益
        predictNextYearPe=json_data['predictNextYearPe']#2020盈利预测市盈率
        indvInduName=json_data['indvInduName']#板块
        publishDate=json_data['publishDate']#发布日期
        item=(stockCode+'\t',stockName,title,emRatingName,sRatingName,orgSName,count,predictNextYearEps,predictNextYearPe,indvInduName,publishDate)
        print(item)
        await write(item)

async def write(item):
    if os.path.exists('研报数据.csv'):
        f = open('研报数据.csv', mode='a', encoding='utf-8-sig', newline='')
        w = csv.writer(f)
        w.writerow(item)
    else:
        f = open('研报数据.csv', mode='a', encoding='utf-8-sig', newline='')
        w = csv.writer(f)
        w.writerow(['股票代码', '股票名称', '研报名称', '原文评级', '评级变动', '机构', '近一月个股研报数', '2020盈利预测收益', '2020盈利预测市盈率', '板块', '发布日期'])
        w.writerow(item)


async def download(url,sem):
    async with sem:
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)
            await parse(html)


if __name__ == "__main__":
    urls=['http://reportapi.eastmoney.com/report/list?industryCode=*&pageSize=50&industry=*&rating=&ratingChange=&beginTime=2018-04-29&endTime=2020-04-29&pageNo={}&qType=0'.format(i) for i in range(1,1268)]
    loop = asyncio.get_event_loop()
    semaphore = asyncio.Semaphore(500)
    tasks = [asyncio.ensure_future(download(url,semaphore)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)
