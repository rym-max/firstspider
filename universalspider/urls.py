# -*- coding=utf-8 -*-
import csv
import re
import requests
import time
from datetime import datetime
import json
from os.path import realpath, dirname
from .utils import get_keyword

#日后再考虑既有page又有keywords
#这部分需重新考虑，完成后删除这条注释


def fromfunc(formatter,start,end,*args):
    for page in range(start, end+1):
        yield formatter % page


def fromfile(filename,formatter,num,*args):

    path = dirname(realpath(__file__)+'/files/'+filename)
    with open(path,'r',encoding='gbk') as f: #使用csv/excel文件
        csv_reader = csv.reader(f)
        for line in csv_reader:
            yield formatter % tuple(line[0:num])

def fromname(filename,formatter,num,*args):

    target_name, keywords = get_keyword(filename)
    for name in target_name.keys():
        yield formatter % name

def fromajax(url, code1, pattern, re_mode, formatter, group_num, need_unix,**kwargs):
    
    data_response = requests.get(url) #headers之后
    api = re.search(pattern, data_response.content.decode(code1),eval(re_mode)).group(group_num)

    if need_unix:
        yield formatter % (api, int(time.time()))
    else:
        yield formatter % (api)

def fromasp(api,regex,*args):
    pass


#采用
def fromdate(website, formatters):
    now_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    times = now_time.split("-")
    value_date ={
        "YYYY":times[0],
        "mm":times[1],
        "dd":times[2],
        "HH":times[3],
        "MM":times[4],
        "SS":times[5],
        "YY":times[0][2:4],
        "m":str(int(times[1])),
        "d":str(int(times[2]))
    }

    for ff in formatters:
        yield ff % value_date

#采用
def fromjson(url, pattern, code1, re_mode, group_num, formatter, code2, need_unix, key1, key2):
    data_response = requests.get(url) #headers之后
    api = re.search(pattern, data_response.content.decode(code1),eval(re_mode)).group(group_num)

    if need_unix:
        data_json = requests.get(formatter % (api, int(time.time()))).content.decode(code2)
    else:
        data_json = requests.get(formatter % api).content.decode(code2)

    data_dict = json.loads(data_json)

    # print("Look here:",isinstance(data_dict,dict))
    # print(data_dict)
    # for k, v in data_dict.items():
    #     print(k)
    
    for ddd in data_dict.get(key1,[]):
        print(ddd)
        if ddd.get(key2,None) is not None:
            yield ddd.get(key2)

def getdate():
    return [datetime.now().strftime("%Y-%m-%d")]