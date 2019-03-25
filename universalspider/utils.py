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

from os.path import realpath, dirname
import json
from csv import reader
from collections import defaultdict
from .configs.configs import configs
import pymysql
import pymssql
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from config_INFO import (CONFIG_HOST, CONFIG_DB, CONFIG_PORT, CONFIG_PSWD, 
    CONFIG_TABLE, CONFIG_USER)

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

    sql_string = r"SELECT config_string FROM config_table WHERE config_name=%(name)s"
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

    sql_string = r"SELECT rule_string FROM config_table WHERE config_name=%(name)s"
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