import requests
import re
import os

url = 'https://msdn.itellyou.cn/'

index_url = 'https://msdn.itellyou.cn/Category/Index'

lang_url = 'https://msdn.itellyou.cn/Category/GetLang'

# 3个参数
list_url = 'https://msdn.itellyou.cn/Category/GetList'

product_url = 'https://msdn.itellyou.cn/Category/GetProduct'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
           'Referer': 'https://msdn.itellyou.cn/'}

def get_post(url,data):
    try:
        r = requests.post(url, data=eval(data), headers=headers)
        r.raise_for_status()
        return r.text  # 返回Unicode型的数据
    except:
        print("POST Error!")

def get_get(url):
    try:
        r = requests.get(url, headers=headers)
        return r
    except:
        print("GET Error!")

def list_id(id_max):
    str_id = []

    for id_min in id_max:
        str_id.append('{"id":"'+str(id_min)+'"}')    # 在列表末尾添加新对象

    return str_id

def re1(in_1,data_1):
    if in_1 == 1:
        retu = re.findall(' data-loadmenu="true" data-menuid="(.*?)" data-target=', data_1.text)
    elif in_1 == 2:
        retu = re.findall('{"id":"(.*?)","name":"', data_1)
    else :
        print("Error!")

    return retu

# main
# main

index_html = get_get(url)

url_1 = re1(1,index_html)

url_1_id_data = list_id(url_1)

for url_1_id_data_min in url_1_id_data:
    print(url_1_id_data_min)
    print("\n")
    class_1_json = get_post(index_url,url_1_id_data_min)
    print(class_1_json)
    print("\n")
    cs = re1(2,class_1_json)
    print(cs)
    
    