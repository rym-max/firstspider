#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   urls.py
@Time    :   2019/04/06 11:40:29
@Author  :   Hzx 
@Version :   1.0
@Contact :   hzxstarcloud@hotmail.com
@Desc    :   None
'''

import csv
import re
import requests
import time
import datetime
import json
from os.path import realpath, dirname
from .utils import get_keyword, get_date_withzone, make_request

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
    now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
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
    return [datetime.datetime.now().strftime("%Y-%m-%d")]

#below new util function
def number_strs(digits,number):
    n = int(number)
    if n >= 10 ** digits:
        return str(n)
    n += 10**digits
    n_l = list(str(n))
    n_l[0]="0"
    return "".join(n_l)

def format_date(date,formatter):
    now_time = date.strftime("%Y-%m-%d-%H-%M-%S")
    yy = now_time.year
    year_start_time = datetime.datetime(yy,1,1,0,0,0)
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
        "d":str(int(times[2])),
        "days": str((now_time - year_start_time).days + 1),
        "days-1":str((now_time - year_start_time).days),
        "UNIX":str(int(time.mktime(now_time.timetuple())))
    }
    return formatter % value_date

def format_number(formatter,number=0,digits=0):
    ff = formatter
    nn = number
    dd = digits
    n_str = number_strs(dd,nn)
    return ff % {"number":n_str}

#below return start_urls list
def URLSZERO(dt,timezone,logger,**kwargs):
    '''time formatter, e.g. daily newspaper
        dt      :date
        spider  :logger
        kwargs  :formatter,start_hour

        description: 
        判断上次时间是不是超过起始时间，超过则调整循环第一天，不找过加一天循环；
        判断这次时间是不是超过起始时间，不超过则减一天循环
    '''
    current_date = get_date_withzone(datetime.datetime.now(),timezone)
    last_date = get_date_withzone(dt,timezone)
    time_delta = current_date - last_date
    day_difference = time_delta.days
    second_difference = time_delta.seconds
    seconds_now = current_date.hour * 3600 + current_date.minute * 60 + current_date.second 

    start_hour = kwargs.get('start_hour',8) #判断起始时间
    oneday_delta = datetime.timedelta(1,0,0)
    
    first_date = last_date
    day_loop = day_difference

    if second_difference > second_difference:
        day_difference +=1

    if last_date.hour >= start_hour:
        first_date += oneday_delta
    else:
        day_loop += 1
    
    if current_date.hour < start_hour:
        day_loop -= 1

    loop_date = first_date
    formatter = kwargs['formatter']
    results = []
    for _ in range(0,day_loop):
        results.append(format_date(loop_date,formatter))
        loop_date += oneday_delta
    
    return results
    

def URLSONE(dt,timezone,logger,**kwargs):
    ''' use time_difference to give a group of number to format, like paging
        dt      :date
        spider  :logger
        kwargs  :
            pageargs:[{
                formatter:,
                pages:[start_number,ratio(page/days),last_page,digits]
            }]

        description:
        根据天数计算页数 将页数匹配进数字 同样适用全静态
        问题 01和1两个区别怎么办 number_strs digits
    '''
    current_date = get_date_withzone(datetime.datetime.now(),timezone)
    last_date = get_date_withzone(dt, timezone)
    time_delta = current_date - last_date
    day_difference = time_delta.days + 1 #可能少个一天，按大的算

    results = []

    for li in kwargs.get("pageargs",[]):
        formatter = li.get('formatter',"")
        pages = li.get('pages',"")
        if pages:
            start_number = [0]
            ratio = pages[1]
            last_page = pages[2]
            digits = pages[3]

            page_difference = int(day_difference * ratio) + 1
            pa_di = page_difference if page_difference < last_page else last_page
            for i in range(start_number, start_number + pa_di):
                results.append(format_number(formatter,i,digits))
        else:
            results.append(format_number(formatter,0,0))
                
    return results

def URLSTWO(dt,timezone,logger,**kwargs):
    '''use time_difference to select a url list
        dt      :date
        spider  :logger
        kwargs  :
            pageargs:[{
                "0":today_url
                "1":yesterday_url
                ...
                "max":7
            }]

        description:
        根据天数选网页，0表示今天 1表示昨天 ...
    '''
    current_date = get_date_withzone(datetime.datetime.now(),timezone)
    last_date = get_date_withzone(dt, timezone)
    time_delta = current_date - last_date
    day_difference = time_delta.days + 1
    
    results = []
    for li in kwargs.get("pageargs",[]):
        dd = day_difference if day_difference < li.get("max",7) else li.get("max",7)
        for i in range(0,day_difference+1):
            url = li.get(str(i),"")
            if url:
                results.append(url)
    
    return results

def URLSTHREE(dt,timezone,logger,**kwargs):
    '''paging,need to set depth;use two
        dt      :date
        spider  :logger
        kwargs  :value
    '''


def URLSFOUR(dt,timezone,logger,**kwargs):
    '''get date from api
        dt      :date
        timezone:timezone
        spider  :logger
        kwargs  :
            api_li :[{
                "api_formatter":
                "pattern_str":{"json_formatter":"","xml_formatter":""}
            }]

        description: 这个最麻烦 谨慎
        api返回json或html或xml格式数据，此处将返回数据中所有url正则匹配下来或读取为
        json文件，以所有url为start_url，故不在去重范围，但理论上不重复
        只做xml与json的转换识别为dict
    '''
    current_date = get_date_withzone(datetime.datetime.now(),timezone)
    
    results = []
    for li in kwargs.get("api_li",[]):
        api_url = format_date(current_date,li.get("api_formatter",""))
        if api_url:
            status_code, res = make_request(api_url,logger,"json",None,60,
                **li.get("pattern_str",{}))
            if status_code in [202, 200]:
                lis = res.get(li.get("itemname","item"),[])
                for ls in lis:
                    item_url = ls.get(li.get("itemurl","url"),"")
                    if item_url:
                        results.append(item_url)

    return results

def get_start_urls(dt,timezone,case,logger,**kwargs):
    '''for start_urls


    '''
    if case == 0:
        #static
        try:
            return URLSZERO(dt,timezone,logger,**kwargs)
        except Exception as e:
            logger.warn(e)

    elif case == 1:
        #loop for number
        try:
            return URLSONE(dt,timezone,logger,**kwargs)
        except Exception as e:
            logger.warn(e)

    elif case == 2:
        #need date
        try:
            return URLSTWO(dt,timezone,logger,**kwargs)
        except Exception as e:
            logger.warn(e)
    elif case == 3:
        #from josn
        try:
            return URLSTHREE(dt,timezone,logger,**kwargs)
        except Exception as e:
            logger.warn(e)

    else:
        
        return []
    
    return []