#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   items.py
@Time    :   2019/03/23 18:57:51
@Author  :   Hzx 
@Version :   1.0
@Contact :   hzxstarcloud@hotmail.com
@Desc    :   None
'''

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UniversalspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(scrapy.Item):
    
    title = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    datetime = scrapy.Field()
    source = scrapy.Field()
    website = scrapy.Field()
    attrs = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    keywords = scrapy.Field()
    dcdescription = scrapy.Field()

    
class BaikeItem(scrapy.Item):

    name = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()