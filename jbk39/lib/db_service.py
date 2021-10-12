'''
Author: mfuture@qq.com
Date: 2021-10-12 14:33:50
LastEditTime: 2021-10-12 17:15:58
LastEditors: mfuture@qq.com
Description:  执行数据库操作
FilePath: /jbk39/jbk39/lib/db_service.py
'''
#! /usr/bin/python
# -*- coding: UTF-8 -*-

 
from .config.pymysql import UsingMysql
import random

# with UsingMysql(log_time=True) as um:


class database():
    def select(table,data): 
        with UsingMysql(log_time=True) as um:
            um.cursor.execute("select count(id) as total from diagnosis")
            data = um.cursor.fetchone()
            print("-- 当前数量: %d " % data['total'])
    def create(table,item):
        with UsingMysql(log_time=True) as um:
            sql="insert into %s values( null,'%s')" %(table,item['name'][0])
            um.cursor.execute(sql)
            # data = um.cursor.fetchone()
            print("【%s】增加成功" %(item['name'][0]))
