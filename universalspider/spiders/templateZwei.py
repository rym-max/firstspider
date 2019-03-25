# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..rules import rules
from ..utils import get_config
from ..itemloader import *
from ..items import *
from .. import urls

class TemplatezweiSpider(CrawlSpider):
    name = 'templateZwei'
    #模板2
    #适用于起始/目录页面动态
    #不需要登录

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('_name',self.name)   #建议考虑scrapyd 从此处获取spider名
        config = get_config(self._name)
        self.config = config
        
        #self.custom_settings = config.get('settings')   #自定义settings覆盖
        self.logger.info('Show the custom_settings %s', str(self.custom_settings))

        self.rules = rules.get(config.get('rules'),()) #建议rules 通用化
        #self.start_urls = config.get('start_urls')
        self.allowed_domains = config.get('allowed_domains',[])
        
        start_urls = config.get('start_urls',{})
        if start_urls.get('type') == 'static':
            self.start_urls = start_urls.get('value',[])
        elif start_urls.get('type') == 'dynamic':
            self.start_urls = list(eval('urls.' + start_urls.get('method'))(**start_urls.get('args',{})))
        
        super(TemplatezweiSpider, self).__init__(*args,**kwargs)

    def parse_item(self, response):


        item = self.config.get('item')
        if item:
            univer_cls =eval(item.get('class'))()
            loader = eval(item.get('loader'))(univer_cls, response=response)

            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'),**{'re': extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'),**{'re': extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'),**{'re': extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')),**{'re': extractor.get('re')})
            yield loader.load_item()

        api = self.config.get('api',None)
        if api:
            #method

            #ifget
            pass
            #ifpost

    def parse_next(self, response):

        item