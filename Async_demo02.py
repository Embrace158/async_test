#__author:Administrator  
#data:2020/4/26
import requests
import json
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
country_code={}
yiqingdailyinfo={}
def get_countryinfo(index_url):#获取地区对应代码
    try:
       rep=requests.get(index_url,headers=headers)
       rep.raise_for_status()
       countryinfos=json.loads(rep.text)  #将返回的json数据解码成python对象
       code_list=countryinfos['data']['areaTree']
       for item in code_list:
           name=item['name']
           id=item['id']
           country_code[id]=name
    except:
        print("未得到国家信息")
    return country_code

def get_detailinfo(id):#获取每个地区的详细疫情数据
    try:
        url="https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?"+id
        print(url)
        rep = requests.get(url=url,headers=headers)
        print(rep.status_code)
        rep.raise_for_status()
        detail_infos= json.loads(rep.text)
        data=detail_infos['data']['list']
        for item in data:
            date=item['date']
            today=item['today']
            yiqingdailyinfo[date]=today
    except:
        print("未得到国家的疫情信息")
    return yiqingdailyinfo

def write_infos():#保存数据

    return "保存成功"

if __name__ == '__main__':
    index_url="https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=317573479337"
    country_id_name_info=get_countryinfo(index_url)
    for item in country_id_name_info.items():
        id=item[0]
        name=item[1]
        country_daily_infos=get_detailinfo(id)
        print(country_daily_infos)


