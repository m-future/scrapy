'''
Author: mfuture@qq.com
Date: 2021-10-12 14:33:50
LastEditTime: 2021-10-14 08:53:46
LastEditors: mfuture@qq.com
Description:  执行数据库操作
FilePath: /health39/jbk39/lib/db_service.py
'''
#! /usr/bin/python
# -*- coding: UTF-8 -*-


from .config.pymysql import UsingMysql
import random
import json

# with UsingMysql(log_time=True) as um:


class database():
    def select(table, data):
        with UsingMysql(log_time=True) as um:
            um.cursor.execute("select count(id) as total from diagnosis")
            data = um.cursor.fetchone()
            print("-- 当前数量: %d " % data['total'])

    def create_diagnosis(table, item):
        with UsingMysql(log_time=True) as um:
            identify = json.dumps(item['identify'], ensure_ascii=False)
            diagnosis = json.dumps(item['diagnosis'], ensure_ascii=False)

            sql = "insert into %s(department,`name`,identify,diagnosis) values('%s','%s','%s','%s')" % (
                table, item['department'], item['name'], identify, diagnosis)
            um.cursor.execute(sql)
            print("诊断-【%s】创建成功" % (item['name']))

    def update_treat(table, item):
        with UsingMysql(log_time=True) as um:
            try:
                identify = json.dumps(item['common_treat'], ensure_ascii=False)
                diagnosis = json.dumps(item['chinese_med_treat'], ensure_ascii=False)
            except Exception as e:
                print(e)

            sql = "update %s set common_treat='%s', chinese_med_treat='%s' where `name`= '%s' " % (
                table, identify, diagnosis, item['name'])
            um.cursor.execute(sql)
            print("诊疗-【%s】更新成功" % (item['name']))

    def update_intro(table, item):
        with UsingMysql(log_time=True) as um:

            sql = "update %s set alias='%s', introduction='%s' where `name`= '%s' " % (
                table, item['alias'], item['intro'], item['name'])
            um.cursor.execute(sql)
            print("简介-【%s】更新成功" % (item['name']))


    def create_section( item):
        with UsingMysql(log_time=True) as um:

            item=item["department"]
   

            sql = "insert into section (pinyin,chinese_name,parent) values('%s','%s','%s')" % (
                item['pinyin'], item['chinese_name'], item['parent'])
            um.cursor.execute(sql)
            print("科室-【%s】创建成功" % (item['chinese_name']))