import requests
import re
import xlwt
import json

url = 'https://msdn.itellyou.cn/'       # 主页
index_url = 'https://msdn.itellyou.cn/Category/Index'       # 请求第一大类下第二大类列表，例：操作系统
lang_url = 'https://msdn.itellyou.cn/Category/GetLang'      # 返回windows 10各语言版本
# 返回windows 10该语言版本所有镜像列表及各镜像部分详情
list_url = 'https://msdn.itellyou.cn/Category/GetList'
# 返回该镜像所有详情，含SHA1,文件大小，发布时间
product_url = 'https://msdn.itellyou.cn/Category/GetProduct'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
           'Referer': 'https://msdn.itellyou.cn/'}


def get_post(url, data):     # post请求，data类型为str
    try:
        # eval()用来将str类型转为dict类型
        r = requests.post(url, data=eval(data), headers=headers)
        r.raise_for_status()
        return r.text  # 返回Unicode型的数据
    except:
        print("post error!")


def get_get(url):       # get请求
    try:
        r = requests.get(url, headers=headers)
        return r
    except:
        print("get error!")


# 用来将一大串id格式化成列表输出，例如：['aaa','bbb']变['{"id":"aaa"}', '{"id":"bbb"}']
def listt(id_sx):
    index = []

    for idd in id_sx:
        index.append('{"id":"'+str(idd)+'"}')    # 在列表末尾添加新对象

    return index

###############################

###############################


res = get_get(url)

# all_cs = re.findall('data-target="#collapse_.*?">(.*?)</a></h4></div><div id="',res.text)   # .*?匹配任意字符，()将匹配的内容提取出来
all_index = re.findall(' data-loadmenu="true" data-menuid="(.*?)" data-target=', res.text)   # 筛选出各大类id

index_ret = listt(all_index)        # 格式化字符串
cs = get_post(index_url, index_ret[0])

print(cs)

json_index = re.findall('{"id":"(.*?)"', str(cs))       # 将接收到的json用正则提取id

str_index = listt(list(json_index))

cs_2 = get_post(lang_url, str_index[0])

print(cs_2)

json_lang = re.findall('{"id":"(.*?)"', str(cs_2))       # 将接收到的json用正则提取id

str_lang = "{'id':'d15691d5-9208-4a7b-b8f8-b64cf6fb875a','lang':'e15db4de-c094-4c50-822a-98ad50daba4f','filter':'true'}"


cs_3 = get_post(list_url, str_lang)

json_list = re.findall('{"id":"(.*?)"', str(cs_3))       # 将接收到的json用正则提取id

str_product = listt(list(json_list))

cs_4 = get_post(product_url, str_product[0])



