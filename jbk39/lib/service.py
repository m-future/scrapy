'''
Author: mfuture@qq.com
Date: 2021-10-12 14:33:50
Description:  执行数据库操作
FilePath: /health39/jbk39/lib/service.py
'''
#! /usr/bin/python3
# -*- coding: UTF-8 -*-


from jbk39.lib.config.mysql import UsingMysql
import random
import json


class DatabaseService():

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
    def select_department(departments='ALL'):
        with UsingMysql(log_time=True) as um:
            if departments == 'ALL':  # 全部科室
                # NOTE: 如果有下级科室，则选择下级科室，比如不选fuchanke, 而是选择fuke,chanke
                sql = 'select pinyin, chinese_name from department where pinyin not in \
                ( select t.parent from (select parent from department ) as t \
                where t.parent is not null )'
                um.cursor.execute(sql)
                data = um.cursor.fetchall()
                return data
            else:  # 部分科室
                # # 格式化字符串，使其符合 mysql 语法
                # department = map(lambda x: "'{}'".format(x), department)
                # department = ",".join(department)
                # sql = "select pinyin, chinese_name from department where parent in (%s) " % (
                #     department)
                # um.cursor.execute(sql)
                # FIXME: 这里只适用于两级部门，多级部门另外逻辑
                result = []
                for department in departments:
                    # 先查找其下级部门
                    sql = "select pinyin, chinese_name from department where parent = '%s' " % (
                        department)
                    um.cursor.execute(sql)
                    data = um.cursor.fetchall()
                    if len(data) == 0:  # 没有下级部门，则选择自己
                        sql = "select pinyin, chinese_name from department where pinyin = '%s' " % (
                            department)
                        um.cursor.execute(sql)
                        data = um.cursor.fetchall()
                    result.extend(data)
                return result

    # 随机选取一个代理 ip
    def select_random_proxy(oldProxy=None):
        with UsingMysql(log_time=True) as um:
            if oldProxy:  # 弃用旧ip，启用新ip
                ip = oldProxy.split('/')[2].split(':')[0]
                um.cursor.execute(
                    "update ip_proxy set available = 0, failed_times=failed_times+1 where ip= '%s'" % (ip))

            # TODO: 选择代理的方式有待改进
            # 这里要注意不要用代理网站的ip去爬代理网站！
            um.cursor.execute(
                "select ip, port from ip_proxy where available=1")
            # um.cursor.execute(
            #     "select ip, port from ip_proxy where available=1 order by id")

            ipproxy = um.cursor.fetchone()

            if ipproxy:
                newProxy = "http://{}:{}".format(
                    ipproxy['ip'], ipproxy['port'])
                return newProxy
            else:
                raise ValueError('no more proxy in the ip pool!')

    # 创建代理ip
    def create_ipproxy(item):
        with UsingMysql(log_time=True) as um:
            item = item["ipproxy"]
            sql = "insert into ip_proxy (ip,port,speed) values('%s','%s',%d) ON DUPLICATE KEY UPDATE speed = %d " % (
                item['ip'], item['port'], item['speed'], item['speed'])
            um.cursor.execute(sql)
            print("ipproxy-【%s】创建成功" % (item['ip']))

    # 获取所有代理地址
    def select_proxy():
        with UsingMysql(log_time=True) as um:
            um.cursor.execute('select ip, port from ip_proxy')
            return um.cursor.fetchall()

    # 更新代理地址的可用性
    def update_proxy(proxy, available):
        with UsingMysql(log_time=True) as um:
            um.cursor.execute(
                " update ip_proxy set available = %d where ip = '%s' " % (available, proxy['ip']))
            print(
                'ipproxy -  telnet {} {} 可用性更新成功：{}'.format(proxy['ip'], proxy['port'], available))
            return um.cursor.fetchall()

    # 创建症状
    def create_symptom(table, item):
        with UsingMysql(log_time=True) as um:
            # item = item["ipproxy"]
            sql = "insert into %s (`name`,intro,possible_disease) values('%s','%s','%s')" % (
                table, item['name'], item['intro'], item['possible_disease'])
            um.cursor.execute(sql)
            print("symptom-【%s】创建成功" % (item['name']))

    # 更新症状 - 病因
    def update_symptom_cause(table, item):
        with UsingMysql(log_time=True) as um:
            # item = item["ipproxy"]
            sql = "update %s set cause= '%s' where `name` = '%s' " % (
                table, item['cause'], item['name'])
            um.cursor.execute(sql)
            print("symptom-【%s】病因 更新成功" % (item['name']))

    # 更新症状 - 诊断详述
    def update_symptom_diagnosis(table, item):
        with UsingMysql(log_time=True) as um:
            # item = item["ipproxy"]
            sql = "update %s set diagnosis= '%s' where `name` = '%s' " % (
                table, item['diagnosis'], item['name'])
            um.cursor.execute(sql)
            print("symptom-【%s】诊断详述 更新成功" % (item['name']))

    # 更新症状 - 检查鉴别
    def update_symptom_identify(table, item):
        with UsingMysql(log_time=True) as um:
            # item = item["ipproxy"]
            sql = "update %s set identify = '%s' where `name` = '%s' " % (
                table, item['identify'], item['name'])
            um.cursor.execute(sql)
            print("symptom-【%s】检查鉴别 更新成功" % (item['name']))

    # 更新症状 - 就诊指南
    def update_symptom_treat_guide(table, item):
        with UsingMysql(log_time=True) as um:
            # item = item["ipproxy"]
            sql = "update %s set treat_guide = '%s' where `name` = '%s' " % (
                table, item['treat_guide'], item['name'])
            um.cursor.execute(sql)
            print("symptom-【%s】就诊指南 更新成功" % (item['name']))

    # 创建检查鉴别
    def create_identify(table, item):
        with UsingMysql(log_time=True) as um:
            identify = item["identify"]
            sql = "insert into %s (`name`,introduction,unsuitable_population,notes,index_explain,include_item,disease,symptom,check_affect,check_process) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') " \
                % (table, item['name'], identify['intro'], identify['unsuitable_population'], identify['notes'],
                 identify['index_explain'], identify['include_item'], identify['disease'], identify['symptom'],
                 identify['check_affect'], identify['check_process'])

            um.cursor.execute(sql)
            print("identify-【%s】 创建成功" % (item['name']))
