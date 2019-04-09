#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pipelines.py
@Time    :   2019/03/23 18:59:28
@Author  :   Hzx 
@Version :   1.0
@Contact :   hzxstarcloud@hotmail.com
@Desc    :   None
'''

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymssql
from time import strftime
from .utils import judge_date,get_config
import time
from .config_INFO import (DATA_DB, DATA_HOST, DATA_PORT, DATA_PSWD, DATA_USER,
    SQL_DB, SQL_HOST, SQL_PSWD, SQL_USER)
from .configs import corewords

class UniversalspiderPipeline(object):
    def process_item(self, item, spider):
        return item

#原则上一个item对应一个pipeline

class NewsStandPipeline(object):
    '''

    ITEM        : news
    DATABASE    : mysql
    '''


    def process_item(self, item, spider):

        self.item_count +=1
        tag = False
        title = item.get('title','')
        url = item.get('url','')
        text = item.get('text','')
        date_time = item.get('datetime','1970/01/01')
        source = item.get('source','')
        website = item.get('website','')
        category = item.get('category', '')
        author = item.get('author','')
        keywords = item.get('keywords', '')

        if self.filter:
            for ff in self.filter:
                if ff in title or ff in text:
                    tag=True
                    break
        else:
            tag=True  

        if tag:
            self.related_count +=1
            sql = "INSERT INTO "+self.table+" (`title`,`date`,`description`,`source`,`creator`,`subject`,`url`,`attach`,`CategoryId`) "+ \
                "VALUES (%(title)s,%(date)s,%(description)s,%(source)s,%(creator)s,%(subject)s,%(url)s,%(attach)s,%(CategoryId)s)"

            value_item = {
                "title" : title,
                "url" : url,
                "description" : text,
                "date" : date_time,
                "source" : source,
                "subject" : category,
                "creator" : author,
                "attach" :"",
                "CategoryId":1
            }
            try:
                self.cur.execute(sql,value_item)
                self.cnx.commit()
            except Exception as e:
                print(e)

        if not self.last_time:
            self.last_time = time.time()
            self.logger.info("Crawled %d pages (at %d pages/min), scraped %d items (at %d items/min)" %(
                    int(self.item_count),int(self.item_count-self.last_item),int(self.related_count),int(self.related_count-self.last_related)
            ))
            self.last_related = self.related_count
            self.last_item = self.item_count
        else:
            if time.time()-self.last_time > 60.0:
                
                self.logger.info("Crawled %d pages (at %d pages/min), scraped %d items (at %d items/min)" %(
                    int(self.item_count),int(self.item_count-self.last_item),int(self.related_count),int(self.related_count-self.last_related)
                ))
                self.last_related = self.related_count
                self.last_item = self.item_count
                self.last_time = time.time()
                    
    
    def open_spider(self, spider):
        '''
            读取配置
        '''
        config = get_config(spider._name)
        self.db = config.get("db","spider_tempnews")
        self.spider_name = config.get("spider_name","default")
        self.table = config.get("table",'news')
        
        #根据语言决定关键词
        language = config.get("language",None)
        if language:
            self.filter = corewords.corewords[language]
        else:
            self.filter = []

        self.cnx = pymysql.connect(host=DATA_HOST,user=DATA_USER,password=DATA_PSWD,db=DATA_DB, charset='utf8mb4')
        self.cur = self.cnx.cursor()
        
        self.logger = spider.logger
        self.item_count = 0
        self.last_item = 0
        self.related_count = 0
        self.last_related = 0
        self.last_time = None


class NewsSQLServerPipeline(object):
    '''

    ITEM        : news
    DATABASE    : SQL SERVER 
    '''

    def process_item(self, item):
                
        title = item.get('title','')
        url = item.get('url','')
        text = item.get('text','')
        date_time = item.get('datetime','1970/01/01')
        source = item.get('source','')
        #website = item.get('website','')
        category = item.get('category', '')
        author = item.get('author','')
        #keywords = item.get('keywords', '')

        if self.filter:
            for ff in self.filter:
                if ff in title or ff in text:
                    tag=True
                    break
        else:
            tag=True  

        if tag:
            sql = "INSERT INTO "+self.table+ " (`title`,`date`,`description`,`source`,`creator`,`subject`,`url`,`attach`,`CategoryId`,`dcdescription`) " + \
                "VALUES (%(title)s,%(date)s,%(description)s,%(source)s,%(creator)s,%(subject)s,%(url)s,%(attach)s,%(CategoryId)s,%(dcdescription)s)"

            value_item = {
                "title" : title,
                "url" : url,
                "description" : text,
                "date" : date_time,
                "source" : source,
                "subject" : category,
                "creator" : author,
                "attach" :"",
                "CategoryId":1,
                "dcdescription":""
            }
            try:
                self.cur.execute(sql,value_item)
                self.cnx.commit()
                self.related_count +=1
            except Exception as e:
                print(e)

        if not self.last_time:
            self.last_time = time.time()
            self.logger.info("Crawled %d pages (at %d pages/min), scraped %d items (at %d items/min)" %(
                    int(self.item_count),int(self.item_count-self.last_item),int(self.related_count),int(self.related_count-self.last_related)
            ))
            self.last_related = self.related_count
            self.last_item = self.item_count
        else:
            if time.time()-self.last_time > 60.0:
                
                self.logger.info("Crawled %d pages (at %d pages/min), scraped %d items (at %d items/min)" %(
                    int(self.item_count),int(self.item_count-self.last_item),int(self.related_count),int(self.related_count-self.last_related)
                ))
                self.last_related = self.related_count
                self.last_item = self.item_count
                self.last_time = time.time()    


    def open_spider(self, spider):
        config = get_config(spider._name)
        self.db = config.get("db","Vip_TongJi")
        self.spider_name = config.get("spider_name","default")
        self.table = config.get("table",'temp'+strftime('%Y%m%d%H%M%S')+self.spider_name)#data

        #根据语言决定关键词
        language = config.get("language",None)
        if language:
            self.filter = corewords.corewords[language]
        else:
            self.filter = []

        self.cnx = pymssql.connect(host=SQL_HOST,user=SQL_USER,password=SQL_PSWD,database=SQL_DB)
        self.cur = self.cnx.cursor()
        
        self.logger = spider.logger
        self.item_count = 0
        self.last_item = 0
        self.related_count = 0
        self.last_related = 0
        self.last_time = None





class NewsStandFilterPipeline(object):
    '''filter with last_date

    ITEM        : news
    DATABASE    : mysql
    '''


    def process_item(self, item, spider):

        self.item_count +=1
        tag = False
        title = item.get('title','')
        url = item.get('url','')
        text = item.get('text','')
        source = item.get('source','')
        website = item.get('website','')
        category = item.get('category', '')
        new_date = item.get('datetime', '1970-1-1 00:00:00')
        author = item.get('author','')
        keywords = item.get('keywords', '')

        if self.filter:
            for ff in self.filter:
                if ff in title or ff in text:
                    tag=True
                    break
        else:
            tag=True  

        news_date, tag_date = judge_date(new_date,self.news_date_formatter,self.last_date, self.timezone)

        if tag and (tag_date or not self.need_filter_date):
            self.related_count +=1
            sql = "INSERT INTO "+self.table+" (`title`,`date`,`description`,`source`,`creator`,`subject`,`url`,`attach`,`CategoryId`) "+ \
                "VALUES (%(title)s,%(date)s,%(description)s,%(source)s,%(creator)s,%(subject)s,%(url)s,%(attach)s,%(CategoryId)s)"

            value_item = {
                "title" : title,
                "url" : url,
                "description" : text,
                "date" : news_date.strftime("%Y-%m-%d"),
                "source" : source,
                "subject" : category,
                "creator" : author,
                "attach" :"",
                "CategoryId":1
            }
            try:
                self.cur.execute(sql,value_item)
                self.cnx.commit()
            except Exception as e:
                print(e)

        if not self.last_time:
            self.last_time = time.time()
            self.logger.info("Crawled %d pages (at %d pages/min), scraped %d items (at %d items/min)" %(
                    int(self.item_count),int(self.item_count-self.last_item),int(self.related_count),int(self.related_count-self.last_related)
            ))
            self.last_related = self.related_count
            self.last_item = self.item_count
        else:
            if time.time()-self.last_time > 60.0:
                
                self.logger.info("Crawled %d pages (at %d pages/min), scraped %d items (at %d items/min)" %(
                    int(self.item_count),int(self.item_count-self.last_item),int(self.related_count),int(self.related_count-self.last_related)
                ))
                self.last_related = self.related_count
                self.last_item = self.item_count
                self.last_time = time.time()
                    
    
    def open_spider(self, spider):
        '''
            读取配置
        '''
        config = spider._config
        self.db = config.get("db","spider_tempnews")
        self.spider_name = config.get("spider_name","default")
        self.table = config.get("table",'news')
        
        #根据语言决定关键词
        language = config.get("language",None)
        if language:
            self.filter = corewords.corewords[language]
        else:
            self.filter = []

        self.cnx = pymysql.connect(host=DATA_HOST,user=DATA_USER,password=DATA_PSWD,db=DATA_DB, charset='utf8mb4')
        self.cur = self.cnx.cursor()
        
        self.logger = spider.logger
        self.item_count = 0
        self.last_item = 0
        self.related_count = 0
        self.last_related = 0
        self.last_time = None

        self.last_date = spider.last_date
        self.timezone = spider.timezone
        self.news_date_formatter = config.get('date_formatter',["%Y-%m-%d %H:%M:%S"])
        self.need_filter_date = config.get("need_filter_date",True) #日报


class NewsSQLFilterPipeline(object):
    '''filter date

    ITEM        : news
    DATABASE    : SQL SERVER 
    '''

    def process_item(self, item, spider):
                
        title = item.get('title','')
        url = item.get('url','')
        text = item.get('text','')
        date_time = item.get('datetime','1970-01-01 00:00:00')
        source = item.get('source','')
        #website = item.get('website','')
        category = item.get('category', '')
        author = item.get('author','')
        #keywords = item.get('keywords', '')
        
        if self.filter:
            for ff in self.filter:
                if ff in title or ff in text:
                    tag=True
                    break
        else:
            tag=True  

        news_date, tag_date = judge_date(date_time,self.news_date_formatter,self.last_date, self.timezone)

        if tag and (tag_date or not self.need_filter_date):
            sql = "INSERT INTO "+self.table+ " (`title`,`date`,`description`,`source`,`creator`,`subject`,`url`,`attach`,`CategoryId`,`dcdescription`) " + \
                "VALUES (%(title)s,%(date)s,%(description)s,%(source)s,%(creator)s,%(subject)s,%(url)s,%(attach)s,%(CategoryId)s,%(dcdescription)s)"

            value_item = {
                "title" : title,
                "url" : url,
                "description" : text,
                "date" : news_date.strftime("%Y-%m-%d"),
                "source" : source,
                "subject" : category,
                "creator" : author,
                "attach" :"",
                "CategoryId":1,
                "dcdescription":""
            }
            try:
                self.cur.execute(sql,value_item)
                self.cnx.commit()
                self.related_count +=1
            except Exception as e:
                print(e)

        if not self.last_time:
            self.last_time = time.time()
            self.logger.info("Crawled %d pages (at %d pages/min), scraped %d items (at %d items/min)" %(
                    int(self.item_count),int(self.item_count-self.last_item),int(self.related_count),int(self.related_count-self.last_related)
            ))
            self.last_related = self.related_count
            self.last_item = self.item_count
        else:
            if time.time()-self.last_time > 60.0:
                
                self.logger.info("Crawled %d pages (at %d pages/min), scraped %d items (at %d items/min)" %(
                    int(self.item_count),int(self.item_count-self.last_item),int(self.related_count),int(self.related_count-self.last_related)
                ))
                self.last_related = self.related_count
                self.last_item = self.item_count
                self.last_time = time.time()    


    def open_spider(self, spider):
        config = spider._config
        self.db = config.get("db","Vip_TongJi")
        self.spider_name = config.get("spider_name","default")
        self.table = config.get("table","data")#data

        #根据语言决定关键词
        language = config.get("language",None)
        if language:
            self.filter = corewords.corewords[language]
        else:
            self.filter = []

        self.cnx = pymssql.connect(host=SQL_HOST,user=SQL_USER,password=SQL_PSWD,database=SQL_DB)
        self.cur = self.cnx.cursor()
        
        self.logger = spider.logger
        self.item_count = 0
        self.last_item = 0
        self.related_count = 0
        self.last_related = 0
        self.last_time = None

        self.last_date = spider.last_date
        self.timezone = spider.timezone
        self.news_date_formatter = config.get('date_formatter',["%Y-%m-%d %H:%M:%S"])
        self.need_filter_date = config.get("need_filter_date",True) #日报