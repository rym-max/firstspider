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
