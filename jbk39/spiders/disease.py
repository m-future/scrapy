'''
Author: mfuture@qq.com
Date: 2021-04-27 11:38:22
LastEditTime: 2021-10-16 12:05:06
LastEditors: mfuture@qq.com
Description: 特定科室下疾病内容的爬取
FilePath: /health39/jbk39/spiders/disease.py
'''
import scrapy
import time  # 引入time模块
import logging

from jbk39.items import Jbk39Item
import json
from jbk39.lib.common import StrFunc
import re

from jbk39.lib.service import DatabaseService as db


global count
count = 0


class jbk39(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "disease"  # 定义蜘蛛名

    custom_settings = {
        "DOWNLOAD_DELAY": 0.05  # 覆盖settings 里面的载延迟 ， 利用代理时本身就有较大的延迟，所以此处可以设置小一点，不用担心被封
    }

    # step1: 开始请求
    def start_requests(self):

        print('--start request--')

        departments = db.select_department(['neike']) 

        base_url = "https://jbk.39.net/bw/"

        for department in departments:

            # 定义爬取的链接
            pinyin = department["pinyin"]
            url = '{}{}_t1/'.format(base_url, department["pinyin"])
            meta = {"base_url": base_url, "pinyin": pinyin}
            yield scrapy.Request(url=url, meta=meta, callback=self.init_parse)

    # step2: 获取疾病分页
    def init_parse(self, response):

        base_url = "{}{}_t1_p".format(
            response.meta["base_url"], response.meta["pinyin"])

        print('--init request--')

        pages = response.xpath(
            '//ul[@class="result_item_dots"]/li/span[last()-1]/a/text()')

        # 有页面数据
        if len(pages) > 0:
            pages = int(pages.extract()[0])
        else:
            raise ValueError("no page  count found.")

        for i in range(pages):
            # step2.2: 请求某一分页
            url = "{}{}".format(base_url, str(i+1))
            yield scrapy.Request(url=url, meta=response.meta, callback=self.parse)

    # step3: 获取某一分页的所有疾病
    def parse(self, response):

        print('--start parse--')

        # 获取某一页面下 某疾病 子项目的 url
        diseaseUrls = response.xpath('//*[@class="result_item_top_l"]')
        for item in diseaseUrls:
            # 该病的url，比如 "https://jbk.39.net/jxzgnmy/"

            link = item.xpath('a/@href').extract()[0]

            # # NOTE: 诊断，初始添加，先运行这里
            # yield scrapy.Request(url=link + 'jb', meta=response.meta, callback=self.diagnosis_parse)

            # 简介
            yield scrapy.Request(url=link + 'jbzs', callback=self.intro_parse)

            # 治疗
            yield scrapy.Request(url=link + 'yyzl', callback=self.treat_parse)

            # 症状
            yield scrapy.Request(url=link + 'zztz', callback=self.symptom_parse)

            # 病因
            yield scrapy.Request(url=link + 'blby', callback=self.cause_parse)

    # ==============================  step4: 以下均为页面解析  =============================

    # 简介

    def intro_parse(self, response):

        item = Jbk39Item()
        name = response.xpath('//div[@class="disease"]/h1/text()').extract()[0]
        intro = response.xpath('//p[@class="introduction"]').extract()[0]
        txt = response.xpath(
            '//span[@class="disease_basic_txt"]/text()').extract()

        alias = txt[1].strip() if len(txt) > 1 else ''

        item['intro'] = StrFunc().cleanStr(intro)
        item['alias'] = alias
        item['classify'] = 'intro'
        item['name'] = name
        yield item

    # 治疗
    def treat_parse(self, response):

        item = Jbk39Item()

        name = response.xpath('//div[@class="disease"]/h1/text()').extract()[0]

        common_treat = []
        chinese_med_treat = []
        flag = 1  # 1、西医治疗； 2、中医治疗
        text_lists = response.xpath(
            '//p[@class="article_name"] | //p[@class="article_content_text"]').extract()

        for text in text_lists:
            mystr = StrFunc().cleanStr(text)
            if mystr.find('中医治疗') >= 0:
                flag = 2

            if mystr.find("西医治疗") < 0 and mystr.find("中医治疗") < 0:

                if flag == 1:
                    common_treat.append(mystr)
                else:
                    chinese_med_treat.append(mystr)

        item["common_treat"] = common_treat
        item["chinese_med_treat"] = chinese_med_treat
        item['classify'] = 'treat'
        item['name'] = name

        yield item

    # 症状
    def symptom_parse(self, response):
        global count

        item = Jbk39Item()

        name = response.xpath('//div[@class="disease"]/h1/text()').extract()[0]

        symptom = []
        text_lists_symptom = response.xpath(
            '//div[@class="article_box"]//p').extract()

        for text in text_lists_symptom:
            mystr = StrFunc().cleanStr(text)
            symptom.append(mystr)

        item["symptom"] = symptom
        item['classify'] = 'symptom'
        item['name'] = name

        count = count+1
        print('count symptom : %d' % (count))

        yield item

    # 病因
    def cause_parse(self, response):

        item = Jbk39Item()

        name = response.xpath('//div[@class="disease"]/h1/text()').extract()[0]

        cause = []
        text_lists_cause = response.xpath(
            '//div[@class="article_box"]//p').extract()

        for text in text_lists_cause:
            mystr = StrFunc().cleanStr(text)
            cause.append(mystr)

        item["cause"] = cause
        item['classify'] = 'cause'
        item['name'] = name

        yield item

    # 鉴别（诊断）
    def diagnosis_parse(self, response):
        # print('goto diagnosis_parse')
        item = Jbk39Item()

        # 疾病名称
        name = response.xpath('//div[@class="disease"]/h1/text()').extract()[0]
        diagnosis = []  # 诊断
        identify = []  # 鉴别

        text_lists_diagnosis = response.xpath(
            '//div[@class="art-box"]/p').extract()
        text_lists_identify = response.xpath(
            '//div[@class="article_paragraph"]/p ').extract()

        for text in text_lists_diagnosis:
            mystr = StrFunc().cleanStr(text)
            diagnosis.append(mystr)

        for text in text_lists_identify:
            mystr = StrFunc().cleanStr(text)
            identify.append(mystr)

        item["diagnosis"] = diagnosis
        item["identify"] = identify
        item["name"] = name
        item['department'] = response.meta["pinyin"]
        item['classify'] = 'diagnosis'

        yield item
