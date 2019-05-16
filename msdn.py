import requests
import re
import os

url = 'https://msdn.itellyou.cn/'
index_url = 'https://msdn.itellyou.cn/Category/Index'
lang_url = 'https://msdn.itellyou.cn/Category/GetLang'
list_url = 'https://msdn.itellyou.cn/Category/GetList'
product_url = 'https://msdn.itellyou.cn/Category/GetProduct'

data = {'id' : 'aff8a80f-2dee-4bba-80ec-611ac56d3849'}  # 企业解决方案
data1 = {'id' : '23958de6-bedb-4998-825c-aa3d1e00d097'}  # MSDN 技术资源库
data2 = {'id' : '95c4acfd-d1a6-41fe-b14d-a6816973d2aa'}  # 工具和资源
data3 = {'id' : '051d75ee-ff53-43fe-80e9-bac5c10fc0fb'}  # 应用程序
data4 = {'id' : 'fcf12b78-0662-4dd4-9a82-72040db91c9e'}  # 开发人员工具
data5 = {'id' : '7ab5f0cb-7607-4bbe-9e88-50716dc43de6'}  # 操作系统
data6 = {'id' : '36d3766e-0efb-491e-961b-d1a419e06c68'}  # 服务器
data7 = {'id' : '5d6967f0-b58d-4385-8769-b886bfc2b78c'}  # 设计人员工具




headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36','Referer': 'https://msdn.itellyou.cn/'}

def get_ilt(url,data,headers):  # data必须为dict类型，可以用eval(str)将str转为dict
    r = requests.post(url,data = data,headers = headers)
    r.raise_for_status()
    return r.text

def dowload(index_res):
    index_id = re.findall(r'{(.*?),"name".*?},',index_res)
    
    for i in index_id:
        dic = '{' + i +'}'
        data_ = eval(dic)
        lang_res = get_ilt(lang_url,data_,headers)
        # print(lang_res)
        lang_id = re.findall('{"status":true,"result":\[{"id":"(.*?)","lang":.*?}]}',lang_res)
        #print(lang_id)
        if lang_id:     # 过滤掉空值
            data_['lang'] = lang_id[0]
            data_['filter'] = 'true'
            #print(data_)
            list_res = get_ilt(list_url,data_,headers)
            #print(list_res)
            product_id = re.findall('{"status":true,"result":\[(.*?),"name":.*?',list_res)
            #print(product_id)
            product_id_ = product_id[0] +'}'
            #print(product_id_)
            product_data = eval(product_id_)
            product_res = get_ilt(product_url,product_data,headers)
            file_name = re.findall('{"status":true,"result":{"FileName":(.*?),"DownLoad":.*?',product_res)
            #print(file_name)
            path = file_name[0][1:-4] + '.txt'          #构造文件名
            #print(path)
            
            with open(path,'w') as f:
                f.write(product_res)
                print(file_name,':下载完成')

def dowload_all():
    res = requests.get(url,headers = headers)

    all_index = re.findall(' data-loadmenu="true" data-menuid="(.*?)" data-target=',res.text)   # 筛选出各大类id
    #print(index_ids)
    for id in all_index:
        data['id'] = id         # 组合id，例：data = {'id': 'aff8a80f-2dee-4bba-80ec-611ac56d3849'} id = aff8a80f-2dee-4bba-80ec-611ac56d3849
        #print(data)
        index_res = get_ilt(index_url, data, headers)
        dowload(index_res)

os.chdir(r"txt")
dowload_all()

res = requests.get(url,headers = headers)

all_index = re.findall(' data-loadmenu="true" data-menuid="(.*?)" data-target=',res.text)


data['id'] = all_index[0]

index_res = get_ilt(index_url, eval("{'id': 'aff8a80f-2dee-4bba-80ec-611ac56d3849'}"), headers)

i = type(data)

# print(i)

print(index_res)