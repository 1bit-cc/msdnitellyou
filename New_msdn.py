import requests
import re
import xlwt
import json

url = 'https://msdn.itellyou.cn/'       # 主页
index_url = 'https://msdn.itellyou.cn/Category/Index'       # 请求第一大类下第二大类列表，例：操作系统
lang_url = 'https://msdn.itellyou.cn/Category/GetLang'      # 返回windows 10各语言版本
list_url = 'https://msdn.itellyou.cn/Category/GetList'      # 返回windows 10该语言版本所有镜像列表及各镜像部分详情
product_url = 'https://msdn.itellyou.cn/Category/GetProduct'        # 返回该镜像所有详情，含SHA1,文件大小，发布时间

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36','Referer': 'https://msdn.itellyou.cn/'}

def get_post(url,data,headers):     # post请求，data类型为str
    try:
        r = requests.post(url,data = eval(data),headers = headers)      # eval()用来将str类型转为dict类型
        r.raise_for_status()
        return r.text       #返回Unicode型的数据
    except:
        print("post error!")

def get_get(url,headers):       # get请求
    try:
        r = requests.get(url,headers = headers)
        return r
    except:
        print("get error!")

def listt(id_sx):       # 用来将一大串id格式化成列表输出，例如：['aaa','bbb']变['{"id":"aaa"}', '{"id":"bbb"}']
    index = []
    x = 0
    for idd in all_index:
        index.append('{"id":"'+str(idd)+'"}')    # 在列表末尾添加新对象
        x = x + 1
    return index

res = get_get(url,headers = headers)

# all_cs = re.findall('data-target="#collapse_.*?">(.*?)</a></h4></div><div id="',res.text)   # .*?匹配任意字符，()将匹配的内容提取出来
all_index = re.findall(' data-loadmenu="true" data-menuid="(.*?)" data-target=',res.text)   # 筛选出各大类id

index_ret = listt(all_index)        # 格式化字符串
cs = get_post(index_url,index_ret[0],headers)

json_index = re.findall('{"id":"(.*?)"',cs)       # 将接收到的json用正则提取id

str_index = listt(list(json_index))
print(str_index)