#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : compile_config_rules.py
@Time : 2019/04/07 15:45:47
@Author : Hzx 
@Version : 1.0
@Contact : hzxstarcloud@hotmail.com
@Desc : compile json file to database
'''

# here put the import lib
import pymysql
import pymssql
import re
import json
import os
import datetime

MYSQL_HOST	="localhost"
MYSQL_DB	="test"
MYSQL_PORT	=3306
MYSQL_PSWD  ="8512"
MYSQL_TABLE ="config_rules"
MYSQL_USER	="user"

SQLSER_HOST	="localhost"
SQLSER_DB	="tempnews"
SQLSER_PORT	=3306
SQLSER_PSWD ="8512"
SQLSER_TABLE="news"
SQLSER_USER	="user"

current_path = os.getcwd() #当前文件夹目录
def compile_config_rules(path=current_path,database="mysql"):
    
    try:
        if database == "mysql":
            cnx = pymysql.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,
            password=MYSQL_PSWD,db=MYSQL_DB,charset="utf8mb4")
            cur = cnx.cursor()
        elif database == "sqlserver":
            cnx = pymssql.connect(host=SQLSER_HOST,user=SQLSER_USER,password=SQLSER_PSWD,
            database=SQLSER_DB)
            cur = cnx.cursor()
    except Exception as e:
        print(e)
        return None

    results = {}
    files= os.listdir(path) #得到文件夹下的所有文件名称

    for ffl in files: #遍历文件夹
        if not os.path.isdir(ffl): #判断是否是文件夹，不是文件夹才打开
            fl = ffl.split("_")
            if fl[-1] == "rules.json":
                name = fl[0]
                with open(path+"/"+ffl,"r",encoding="utf8") as ff:
                    item = {
                        "name":name,
                        "rules":ff.read()
                    }
                if name not in results.keys():
                    results.setdefault(name,item)
                else:
                    results[name].update(item)
            else:
                fm = ffl.split(".")
                if fm[-1] == "json":
                    name = fm[0]
                    with open(path+"/"+ffl,"r",encoding="utf8") as ff:
                        item = {
                            "name":name,
                            "configs":ff.read()
                        }
                    
                    item_config = json.loads(item['configs'])
                    item.update({
                        "daylimit":item_config.get("daylimit","1,3,7")
                    })
                    if name not in results.keys():
                        results.setdefault(name,item)
                    else:
                        results[name].update(item)

                else:
                    print(ffl,"：文件格式不符")

    value_item = {
        "datelast":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    sql_string = "INSERT INTO " + MYSQL_TABLE + \
    " (`name`,`configs`,`rules`,`datelast`,`daylimit`) VALUES" + \
    " (%(name)s,%(configs)s,%(rules)s,%(datelast)s,%(daylimit)s)"

    for k,v in results.items():
        value_item.update(v)
        try:
            cur.execute(sql_string, value_item)
            cnx.commit()
        except Exception as e:
            print("插入数据错误:\n\r <<<<%s" % str(e))
    
    return 1

if __name__ == "__main__":
    result = compile_config_rules()
    if result:
        print("成功结束")