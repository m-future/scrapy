'''
Author: mfuture@qq.com
Date: 2021-10-12 14:33:50
LastEditTime: 2021-10-15 10:03:46
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

            print("%s -【%s】创建成功" % (item["department"], item['name']))

    # 更新疾病-诊断
    def update_treat(table, item):
        with UsingMysql(log_time=True) as um:

            identify = json.dumps(item['common_treat'], ensure_ascii=False)
            diagnosis = json.dumps(
                item['chinese_med_treat'], ensure_ascii=False)
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

    # 更新疾病-病因
    def update_cause(table, item):
        with UsingMysql(log_time=True) as um:
            cause = json.dumps(item['cause'], ensure_ascii=False)
            sql = "update %s set cause='%s' where `name`= '%s' " % (
                table, cause, item['name'])
            um.cursor.execute(sql)

            print("病因-【%s】更新成功" % (item['name']))

    # 更新疾病-症状
    def update_symptom(table, item):
        with UsingMysql(log_time=True) as um:
            symptom = json.dumps(item['symptom'], ensure_ascii=False)

            sql = "update %s set symptom='%s' where `name`= '%s' " % (
                table, symptom, item['name'])

            um.cursor.execute(sql)

            print("症状-【%s】更新成功" % (item['name']))

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
                um.cursor.execute(
                    "select pinyin, chinese_name from department")
            else:
                # 格式化字符串，使其符合 mysql 语法
                department = map(lambda x: "'{}'".format(x), department)
                department = ",".join(department)
                sql = "select pinyin, chinese_name from department where pinyin in (%s) " % (
                    department)
                um.cursor.execute(sql)

            data = um.cursor.fetchall()

            return data

    # 随机选取一个代理 ip
    def random_proxy(proxy):
        with UsingMysql(log_time=True) as um:
            if proxy:  # 弃用旧ip，启用新ip
                ip = proxy.split('/')[2].split(':')[0]
                um.cursor.execute(
                    "update ip_proxy set available = 0, failed_times=failed_times+1 where ip= '%s'" % (ip))

            um.cursor.execute(
                "select ip, port from ip_proxy where available=1 order by rand()")
            return um.cursor.fetchone()

    # 创建代理ip
    def create_ipproxy(item):
        with UsingMysql(log_time=True) as um:
            item = item["ipproxy"]
            sql = "insert into ip_proxy (ip,port,speed) values('%s','%s',%d) ON DUPLICATE KEY UPDATE speed = %d " % (
                item['ip'], item['port'], item['speed'], item['speed'])
            um.cursor.execute(sql)
            print("ipproxy-【%s】创建成功" % (item['ip']))
