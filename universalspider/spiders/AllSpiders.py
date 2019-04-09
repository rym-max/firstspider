#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   AllSpiders.py
@Time    :   2019/03/23 18:46:16
@Author  :   Hzx 
@Version :   1.0
@Contact :   hzxstarcloud@hotmail.com
@Desc    :   ALL need to run spiders are here
'''

from .templateZwei import TemplatezweiSpider


class PeopleSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "people"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1
    }

class RmrbSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "rmrb"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1
    }

class GmwSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "gmw"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1
    }

class CssnSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "cssn"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1
    }

class ChinaSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "china"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1
    }

class FmprcSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "fmprc"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1
    }

class HuanqiuSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "huanqiu"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1
    }

class SpiegelSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "spiegel"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1
    }


class SueddeutscheSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "sueddeutsche"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1,
        "REDIRECT_MAX_TIMES":2
    
    }

class TagesschauSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "tagesschau"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1
    }

class HandelsblattSpider(TemplatezweiSpider):
    '''production scene need exclusive class now

    due to main problem above, should customize custom_settings as attributes and declare its own name
    '''
     
    name = "handelsblatt"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "ITEM_PIPELINES":{
            "universalspider.pipelines.NewsStandFilterPipeline": 300
        },
        "DOWNLOAD_DELAY": 1,
        "DOWNLOADER_MIDDLEWARES" : {
           'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
           'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware':None,
        },
        "HTTPERROR_ALLOWED_CODES":[302]
        # "REDIRECT_ENABLED": False
        # "DEFAULT_REQUEST_HEADERS":{
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'zh-CN,zh;q=0.9',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        # }
    }
