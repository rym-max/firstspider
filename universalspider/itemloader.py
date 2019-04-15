#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   itemloader.py
@Time    :   2019/03/23 19:02:24
@Author  :   Hzx 
@Version :   1.0
@Contact :   hzxstarcloud@hotmail.com
@Desc    :   for item;customize loader
'''

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose
import re

class BaikeShort(object):
    '''

    for short URL of baidu baike
    '''
    def __call__(self, values):
        if re.search(r'.*\?',values):
            return re.search(r'.*\?',values).group().replace("?","")
        else:
            return values

class ESCAPE(object):
    '''

    for debug
    '''
    def __call__(self,values):
        if isinstance(values,str):
            print("是字符串啊")
        return values

class BasicLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ChinaLoader(BasicLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())

class BaikeLoader(BasicLoader):
    text_out = Compose(Join(),lambda s: s.strip())
    title_out = Compose(Join(),lambda s: s.strip())
    url_out = Compose(Join(), BaikeShort())

# class NewsLoader(BasicLoader):
#     text_out = Compose(Join(), lambda s: s.strip(), lambda s: s.replace("\u3000\u3000",""), lambda s: s.replace("\xa0",""), lambda s: s.replace(r"\r\n","<br>"))
#     source_out = Compose(Join(), lambda s: s.strip())
#     # category_out = Compose(Join(),lambda s: s.strip(),lambda s: s.split('.')[0],lambda s: s.split('http://')[-1],lambda s: s.split('https://')[-1])

class NewsLoader(BasicLoader):
    '''

    itemname_in     : 
    itemname_out    : 
    '''
    text_out = Compose(Join(), lambda s: s.strip(),
        lambda s: s.replace("\u3000\u3000",""),
        lambda s: s.replace("\xa0",""),
        lambda s: s.replace(r"\r\n","<br>"))

    source_out = Compose(Join(), lambda s: s.strip())

    def add_re(self,field_name, re_form, *processors, **kw):
        values = self._get_revalues(re_form, **kw)
        return self.add_value(field_name, values, *processors, **kw)
    
    def _get_revalues(self, re_form, **kw):
        pattern = re.compile(re_form ,re.DOTALL)
        if self.context.get('response',None):
            response = self.context.get('response')
            return pattern.search(response, re.DOTALL).group()