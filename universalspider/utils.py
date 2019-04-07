#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2019/03/23 19:19:21
@Author  :   Hzx 
@Version :   1.0
@Contact :   hzxstarcloud@hotmail.com
@Desc    :   
'''

import datetime
import json
import re
from collections import defaultdict
from csv import reader
from os.path import dirname, realpath

#from .configs.configs import configs
import pymysql
import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

import pymssql
from config_INFO import (CONFIG_DB, CONFIG_HOST, CONFIG_PORT, CONFIG_PSWD,
                         CONFIG_TABLE, CONFIG_USER)


def get_date_withzone(tt,timezone=8):
    now_time_zone = 8
    seconds_difference = (timezone - now_time_zone) * 3600
    return tt - datetime.timedelta(0, seconds_difference, 0)


# def get_config(name):
#     '''get configs from .py file

#     due to scrapyd cannot read json file in egg package
#     '''
#     return configs.get(name,{})

def get_config(name):
    '''get config from .json file

    mainly for debug
    '''
    if name:
        print(realpath(__file__))
        path = dirname(realpath(__file__))+'\\configs\\'+name+'.json'
        with open(path,'r', encoding='utf8') as f:
            return json.loads(f.read())
    else:
        return {}

def get_configs(name):
    '''get config from mysql database

    annoying to always change configs.py 
    '''
    cnx = pymysql.connect(host=CONFIG_HOST, user=CONFIG_USER,
        password=CONFIG_PSWD, db=CONFIG_DB, charset="utf8mb4")
    cur = cnx.cursor()

    sql_string = r"SELECT configs FROM " + CONFIG_TABLE + " WHERE name=%(name)s"
    item = {
        "name":name
    }
    result = cur.execute(sql_string,item)
    if result:
        config_string = cur.fetchone()[0]
        config = json.loads(config_string)
        return config
    else:
        return {}

def get_rules(name):
    '''get rules from mysql database

        rule={
            "item":[
                {
                    "linkextra":{
                        "allow":
                        "deny":
                        "restrict_xpath":
                        "restrict_css":
                    },
                    "follow":
                    "callback":
                }
            ]
        }
    '''
    cnx = pymysql.connect(host=CONFIG_HOST, user=CONFIG_USER,
        password=CONFIG_PSWD, db=CONFIG_DB, charset="utf8mb4")
    cur = cnx.cursor()

    sql_string = r"SELECT rules FROM " + CONFIG_TABLE + " WHERE name=%(name)s"
    item = {
        "name":name
    }
    result = cur.execute(sql_string,item)
    if result:
        rule_string = cur.fetchone()[0]
        rules = json.loads(rule_string)
        rrs = []
        for r in rules.get("item",()):
            l = r["linkextra"]
            allow = l["allow"] if l["allow"] else ()
            deny = l["deny"] if l["deny"] else ()
            res_xp = l["restrict_xpath"] if l["restrict_xpath"] else ()
            res_cs = l["restrict_css"] if l["restrict_css"] else ()
            follow = r["follow"] if r["follow"] else None
            callback = r["callback"] if r["callback"] else None
            newR = Rule(LinkExtractor(allow=allow, deny=deny, 
                restrict_xpaths=res_xp, restrict_css=res_cs), 
                callback=callback, follow=follow)
            rrs.append(newR)
        return rrs
    else:
        return () 

def get_dates(name):
    '''get lastdate from mysql database

    '''
    cnx = pymysql.connect(host=CONFIG_HOST, user=CONFIG_USER,
        password=CONFIG_PSWD, db=CONFIG_DB, charset="utf8mb4")
    cur = cnx.cursor()

    sql_string = r"SELECT datetime FROM " + CONFIG_TABLE + " WHERE name=%(name)s"
    item = {
        "name":name
    }
    result = cur.execute(sql_string,item)
    if result:
        date_string = cur.fetchone()[0]
        return date_string
    else:
        return "null"


def get_keyword(file):
    '''read file as keywords

    may use some search engine to search for data

    '''
    path = dirname(realpath(__file__)) + '\\files\\' + file
    with open(path,'r',encoding='gbk') as f:
        csv_reader = reader(f)
        target_name = defaultdict(list)
        keywordlist = []
        line_num = 1
        for line in csv_reader:
            
            #首项关键词判断别名和长名
            name = line[0].replace(')',"").replace('）',"").replace('(',"/").replace('（',"/").replace("、","/").replace('\\',"/").split("/")
            for nn in name:
                target_name[nn].append(line_num)
            
            if line[1:]:
                wordslist = []
                for words in line[1:]:
                    wordslist.extend(words.replace("/"," ").replace("、"," ").split(" "))
                keywordlist.append(wordslist)
            
            line_num += 1

    return target_name,keywordlist


session = requests.Session()
session.headers = {

}
def make_request(url, logger, rtype="html", data=None, timeout=60, **kwargs):

    try:
        if data:
            r = session.post(url, data=data, timeout=timeout)
        else:
            r = session.get(url, timeout=timeout)
        r.encoding = 'utf8'
    except Exception as err:
        logger.warn("<<<<<[%s] request error, [message]: \n\r<<<<<<%s" % (url, str(err)))
        return -1, {}
    else:
        if rtype == "json":
            try:
                r_json = r.json()
            except json.JSONDecodeError as e: 
                logger.debug("<<<<<<[%s] :\n\r <<<<<<decode error:cannot decode json directly \n\r <<<<<<%s" % (url, str(e)))
            else:
                if kwargs.get("json_pattern",""):
                    pattern = kwargs.get("json_pattern","")
                    json_str = re.search(pattern,r.content,re.DOTALL)
                    r_json = json.loads(json_str)
                else:
                    r_json = {}
            return r.status_code, r_json
        elif rtype == "xml":
            return r.status_code, r.text
        elif rtype == "html":
            return r.status_code, r.text
        else:
            return r.status_code, r.text


def json_dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=4, sort_keys=True)
