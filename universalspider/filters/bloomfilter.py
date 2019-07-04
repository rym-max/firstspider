#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   bloomfilter.py
@Time    :   2019/07/02 20:48:52
@Author  :   Hzx 
@Version :   1.0
@Contact :   hzxstarcloud@hotmail.com
@Desc    :   None
'''

# here put the import lib

from pybloom_live import ScalableBloomFilter
import hashlib
import logging

logger = logging.getLogger(__name__)

class Bloomfilter(object):

    logger = None

    def __init__(self,logger=logger,*args,**kwargs):
        self.logger = logger
        self.sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH, error_rate=1e-6)
    
    def setlogger(self,logger=logger):
        #防止读取时logger指向原logger而不存在
        self.logger = logger

    def md5(self, url):
        md5 = hashlib.md5()
        md5.update(url.encode("utf-8"))
        return md5.hexdigest()
    
    def check(self, url):
        url = self.md5(url)
        if url in self.sbf:
            return True
        else:
            return False

    def add_in_sbf(self, url):
        try:
            self.sbf.add(self.md5(url))
        except Exception as e:
            self.logger("[%s] bloomfilter exception<<<<<<<<< [%s]" % (url, str(e)))