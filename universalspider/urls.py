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
from .utils import get_keyword, get_date_withzone, make_request, set_dates

#日后再考虑既有page又有keywords
#这部分需重新考虑，完成后删除这条注释
import logging
default_logger = logging.getLogger(__name__)


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
    if n >= 10 ** (digits-1):
        return str(n)
    n += 10**(digits-1)
    n_l = list(str(n))
    n_l[0]="0"
    return "".join(n_l)

def format_date(date,formatter):
    default_logger.debug("i'm here 4")
    now_time = date.strftime("%Y-%m-%d-%H-%M-%S")
    yy = date.year
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
        "days": str((date - year_start_time).days + 1),
        "days-1":str((date - year_start_time).days),
        "days3": number_strs(3,(date - year_start_time).days + 1),
        "UNIX":str(int(time.mktime(date.timetuple())))
    }
    default_logger.debug("i'm here 5")
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
        spider  :spider
        kwargs  :formatter,start_hour

        description: 
        判断上次时间是不是超过起始时间，超过则调整循环第一天，不找过加一天循环；
        判断这次时间是不是超过起始时间，不超过则减一天循环
    '''
    current_date = get_date_withzone(datetime.datetime.now(),timezone)
    last_date = get_date_withzone(dt,timezone)
    
    oneday_delta = datetime.timedelta(1,0,0)
    logger.debug("i'm here 3")
    results = []
    for li in kwargs.get("pageargs",[]):
        start_hour = li.get("start_hour",None)
        logger.debug("i'm here 4")
        start_date = last_date
        if start_hour:
            if last_date.hour >= start_hour:
                start_date += oneday_delta

            if current_date.hour < start_hour:
                current_str = current_date.strftime("%Y-%m-%d 00:00:00")
            else:
                current_str = (current_date+oneday_delta).strftime("%Y-%m-%d 00:00:00")
        else:
            current_str = current_date.strftime("%Y-%m-%d %H:%M:%S")

        end_date = datetime.datetime.strptime(current_str,"%Y-%m-%d %H:%M:%S")

        loop_date = start_date
        formatter = li['formatter']
        while loop_date < end_date:
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
                pages:[
                    start_number, default 0
                    ratio(page/days), default 0
                    last_page, default 0
                    digits default 0
                    ]
            }]

        description:
        根据天数计算页数 将页数匹配进数字 同样适用全静态
        问题 01和1两个区别怎么办 number_strs digits
    '''
    logger.debug("i'm here 2")
    current_date = get_date_withzone(datetime.datetime.now(),timezone)
    last_date = get_date_withzone(dt, timezone)
    time_delta = current_date - last_date
    day_difference = time_delta.days + 1 #可能少个一天，按大的算
    logger.debug("i'm here 3")
    results = []

    for li in kwargs.get("pageargs",[]):
        formatter = li.get('formatter',"")
        pages = li.get('pages',"")
        logger.debug("i'm here 4")
        if pages:
            start_number = pages[0]
            ratio = pages[1]
            last_page = pages[2]
            digits = pages[3]

            logger.debug("i'm here 5")
            page_difference = int(day_difference * ratio) + 1
            logger.debug("i'm here 6")
            pa_di = page_difference if page_difference < last_page else last_page
            logger.debug("i'm here 7 %s----%s" % (str(start_number), str(pa_di)))
            for i in range(start_number, start_number + pa_di):
                logger.debug("i'm here 8")
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
        for i in range(0,dd+1):
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
    raise ValueError

def URLSFOUR(dt,timezone,logger,**kwargs):
    '''get date from api
        dt      :date
        timezone:timezone
        spider  :logger
        kwargs  :
            api_li :[{
                "api_formatter":[]
                "pattern_str":{"json_formatter":"","xml_formatter":""}
            }]

        description: 这个最麻烦 谨慎
        api返回json或html或xml格式数据，此处将返回数据中所有url正则匹配下来或读取为
        json文件，以所有url为start_url，故不在去重范围，但理论上不重复
        只做xml与json的转换识别为dict
    '''
    logger.debug("i'm here 2")
    current_date = get_date_withzone(datetime.datetime.now(),timezone)
    logger.debug("i'm here 3")
    results = []
    for li in kwargs.get("api_li",[]):
        api_url = li.get("api_formatter",[])
        for apuu in api_url:
            apu = format_date(current_date,apuu)
            status_code, res = make_request(apu,logger,"json",None,60,
                li.get("api_code","utf8"),**li.get("pattern_str",{}))
            logger.debug("response result<<<<%s" % str(res))
            logger.debug("response status<<<<%s" % str(status_code))
            logger.debug("至少在这")
            if status_code in [202, 200]:
                itemls = li.get("itemname",[])
                a = res
                for itl in itemls:
                    logger.debug("last_string <<<<<%s" % str(a.keys()))
                    a = a.get(itl,{})

                if a:
                    for ls in a:
                        item_url = ls.get(li.get("itemurl","url"),"")
                        if item_url:
                            results.append(item_url)

    return results

def URLSFIVE(dt,timezone,logger,**kwargs):
    '''get url from a series api

    dt      :date
    timezone:timezone
    spider  :logger
    kwargs  :
        api_li :[{
            "api_forma":[
                {
                    "formatter":""
                    "pages":[start,ratio,end,step,digit]
                },
                {
                    "formatter":""
                }
            ]
            "pattern_str"   :{"json_formatter":"","xml_formatter":""},
            "api_code"      :
            "itemname"      :
            "itemurl"       :
        }]
    '''
    logger.debug("i'm here 2")
    current_date = get_date_withzone(datetime.datetime.now(),timezone)
    last_date = get_date_withzone(dt, timezone)
    time_delta = current_date - last_date
    day_difference = time_delta.days + 1 #可能少个一天，按大的算
    logger.debug("i'm here 3")
    results = []
    input_args = {"api_li":[]}
    for apili in kwargs.get("api_li",[]):
        valueitem = apili
        page_results = []
    
        for li in apili.get('api_forma',[]):
            formatter = li.get('formatter',"")
            pages = li.get('pages',"")
            logger.debug("i'm here 4")
            if pages:
                start_number = pages[0]
                ratio = pages[1]
                last_page = pages[2]
                step = pages[3]
                digits = pages[4]

                logger.debug("i'm here 5")
                page_difference = int(day_difference * ratio) + 1
                logger.debug("i'm here 6")
                pa_di = page_difference if page_difference < last_page - start_number +1 else last_page - start_number + 1
                logger.debug("i'm here 7 %s----%s" % (str(start_number), str(pa_di)))
                for i in range(start_number, start_number + pa_di, step):
                    logger.debug("i'm here 8")
                    page_results.append(format_number(formatter,i,digits))
            else:
                page_results.append(format_number(formatter,0,0))
        
        valueitem['api_formatter'] = page_results
        input_args["api_li"].append(valueitem)
    
    results.extend(URLSFOUR(dt,timezone,logger,**input_args))
                
    return results


def URLSTEN(dt,timezone,logger,**kwargs):
    '''get date from api
        dt      :date
        timezone:timezone
        spider  :logger
        kwargs  :
            pageargs :[
                {}
            ]

        description: 综合前面的
    '''
    funclist = [
        "URLSZERO",
        "URLSONE",
        "URLSTWO",
        "URLSTHREE",
        "URLSFOUR"
    ]
    alldata = kwargs.get("pageargs",[])
    results = []
    for al in alldata:
        logger.debug('[show some data]<<<< %s' % str(al))
        func_string = funclist[al['case']] if al['case'] < len(funclist) else ""
        logger.debug('')
        if func_string:
            result = eval(func_string)(dt,timezone,logger,**al['Kwargs'])
            results.extend(result)

    return results


def get_start_urls(dt,timezone,case,logger,**kwargs):
    '''for start_urls


    '''
    logger.debug("i'm here 1")
    if case == 0:
        #dateformatter
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
        #select via date
        try:
            return URLSTWO(dt,timezone,logger,**kwargs)
        except Exception as e:
            logger.warn(e)

    elif case == 3:
        #null
        try:
            return URLSTHREE(dt,timezone,logger,**kwargs)
        except Exception as e:
            logger.warn(e)
    elif case == 4:
        #from josn
        try:
            return URLSFOUR(dt,timezone,logger,**kwargs)
        except Exception as e:
            logger.warn(e)
    elif case == 5:
        #a series of api
        try:
            return URLSFIVE(dt,timezone,logger,**kwargs)
        except Exception as e:
            logger.warn(e)
    elif case == 10:
        #综合
        try:
            return URLSTEN(dt,timezone,logger,**kwargs)
        except Exception as e:
            logger.warn(e)
    else:
        
        return []
    
    return []