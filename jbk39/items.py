'''
Author: mfuture@qq.com
Date: 2021-10-14 12:42:00
Description: scrapy item 容器
FilePath: /health39/jbk39/items.py
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Jbk39Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field() # 疾病名
    classify = scrapy.Field() # 分类
    intro = scrapy.Field() # 简介
    alias = scrapy.Field() # 别名
    department = scrapy.Field() # 科室 {"pinyin":"fuke","chinese_name":"妇科","pId":"fuchangke"}
    diagnosis = scrapy.Field() #诊断
    identify = scrapy.Field() #鉴别
    common_treat = scrapy.Field() #一般治疗
    chinese_med_treat = scrapy.Field() #中医治疗
    symptom=scrapy.Field() # 症状
    cause=scrapy.Field() # 病因
    possible_disease=scrapy.Field() # 症状下可能的疾病
    treat_guide=scrapy.Field() # 就诊指南

    ipproxy=scrapy.Field() # 代理IP，反爬

    pass
