'''
Author: mfuture@qq.com
Date: 2021-10-12 14:33:50
LastEditTime: 2021-10-14 12:34:43
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

    # 创建疾病数据库
    def create_diagnosis(table, item):
        with UsingMysql(log_time=True) as um:
            identify = json.dumps(item['identify'], ensure_ascii=False)
            diagnosis = json.dumps(item['diagnosis'], ensure_ascii=False)

            sql = "insert into %s(department,`name`,identify,diagnosis) values('%s','%s','%s','%s')" % (
                table, item['department'], item['name'], identify, diagnosis)
            um.cursor.execute(sql)
            print("%s -【%s】创建成功" % (item["department"],item['name']))

    # 更新疾病-诊断
    def update_treat(table, item):
        with UsingMysql(log_time=True) as um:
            try:
                identify = json.dumps(item['common_treat'], ensure_ascii=False)
                diagnosis = json.dumps(
                    item['chinese_med_treat'], ensure_ascii=False)
            except Exception as e:
                print(e)

            sql = "update %s set common_treat='%s', chinese_med_treat='%s' where `name`= '%s' " % (
                table, identify, diagnosis, item['name'])
            um.cursor.execute(sql)
            print("诊疗-【%s】更新成功" % (item['name']))

    # 更新疾病-简介
    def update_intro(table, item):
        with UsingMysql(log_time=True) as um:

            sql = "update %s set alias='%s', introduction='%s' where `name`= '%s' " % (
                table, item['alias'], item['intro'], item['name'])
            um.cursor.execute(sql)
            print("简介-【%s】更新成功" % (item['name']))

    # 创建科室数据库
    def create_department(item):
        with UsingMysql(log_time=True) as um:
            item = item["department"]
            sql = "insert into department (pinyin,chinese_name,parent) values('%s','%s','%s')" % (
                item['pinyin'], item['chinese_name'], item['parent'])
            um.cursor.execute(sql)
            print("科室-【%s】创建成功" % (item['chinese_name']))

    # 选择科室
    def select_department(department=None):
        with UsingMysql(log_time=True) as um:
            if not department:  # 全部科室
                um.cursor.execute("select pinyin, chinese_name from department")
            else:
                department=",".join(department)
                sql="select pinyin, chinese_name from department where pinyin in (%s) " % (department)
                um.cursor.execute(sql)

            data = um.cursor.fetchall()

            return data
