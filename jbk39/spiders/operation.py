'''
Author: mfuture@qq.com
Date: 2021-10-19 09:52:35
Description: 手术
FilePath: /health39/jbk39/spiders/operation.py
'''

import scrapy
import time  # 引入time模块
import logging

from jbk39.items import Jbk39Item
import json
from jbk39.lib.common import StrFunc
import re

from jbk39.lib.service import DatabaseService as db



class jbk39(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "operation"  # 定义蜘蛛名

    custom_settings = {
        "DOWNLOAD_DELAY": 0.2,  # 覆盖settings 里面的载延迟 ， 利用代理时本身就有较大的延迟，所以此处可以设置小一点，不用担心被封
        "JOBDIR": './jobs/{}'.format(name),
        "USE_IP_PROXY": True
    }

    # step1: 开始请求
    def start_requests(self):

        print('--start request--')

        departments = db.select_department([])

        base_url = "https://jbk.39.net/bw/"

        for department in departments:
            # 症状链接
            pinyin = department["pinyin"]
            url = '{}{}_t4/'.format(base_url, department["pinyin"])
            meta = {"base_url": base_url, "pinyin": pinyin}
            yield scrapy.Request(url=url, meta=meta, callback=self.init_parse)

    # step2: 获取分页数
    def init_parse(self, response):

        base_url = "{}{}_t4_p".format(
            response.meta["base_url"], response.meta["pinyin"])

        print('--init request--')

        pages = response.xpath(
            '//ul[@class="result_item_dots"]/li/span[last()-1]/a/text()')

        # 有页面数据
        if len(pages) > 0:
            pages = int(pages.extract()[0])
        else:
            pages = 1
        
        for i in range(pages):
            # step2.2: 请求某一分页
            url = "{}{}".format(base_url, str(i+1))
            yield scrapy.Request(url=url, meta=response.meta, callback=self.parse)

    # step3: 获取某一分页的所有子类目
    def parse(self, response):

        print('--start parse--')

        elements = response.xpath('//*[@class="result_item_top_l"]')

        
        for ele in elements:
            
            link = ele.xpath('a/@href').extract()[0]

            # NOTE: 综述，初始添加，先运行这里
            yield scrapy.Request(url=link , meta=response.meta, callback=self.parse_intro)

    # ==============================  step4: 以下均为页面解析  =============================

    # 综述
    def parse_intro(self, response):
        # print('goto diagnosis_parse')
        item = Jbk39Item()

        # 疾病名称
        name = response.xpath('//div[@class="ss_det catalogItem"]/div[@class="tit clearfix"]/h1/b/text()').extract()[0]


        # 子项目
        catalogs=[
            {'label':'适应症','col':'indication'},
            {'label':'手术类别','col':'operation_catalog'},
            {'label':'人群','col':'unsuitable_population'},
            {'label':'术前','col':'before_operation'},
            {'label':'手术过程','col':'operative_process'},
            {'label':'术后','col':'after_operation'},
            {'label':'相关疾病','col':'relative_disease'},
            {'label':'相关症状','col':'relative_symptom'},
            ]

        # 提前设定好，避免后续存储时麻烦
        operation = {}
        
        operation['department']=response.meta['pinyin']

        for key in catalogs:
            operation[key['col']]='' if key['label'] in ('intro','department') else []
                

        intro= response.xpath('//div[contains(@class,"des")]/span').extract()[0]


        operation['intro']=StrFunc().str_format(intro)


        elements= response.xpath('//article//div[contains(@class,"lbox")]')

        for ele in elements:

            label= ele.xpath('./div[contains(@class,"clearfix")]/*/text()').extract()[0] # 目录标签
        
            catalog= list(filter(lambda x: label.find(x['label']) > -1, catalogs))[0]

            col=catalog['col'] # 数据库对应的列

            # 疾病或者症状

            if col in ('relative_disease'):
                operation[col]=ele.xpath('.//li/a/text()').extract()
            elif col == 'operative_process':
                data = ele.xpath('.//ul/li').extract()
                result = list(map(lambda x: StrFunc().str_format(x),data))
                operation[col]=result
            elif col == 'operation_catalog':
                data = ele.xpath('.//table//tr[position()>1]/td[position()=1]').extract()
                result = list(map(lambda x: StrFunc().str_format(x),data))
                operation[col]=result
            else:
                data=ele.xpath('.//p | .//div').extract()
                result = list(map(lambda x: StrFunc().str_format(x),data))
                operation[col]=result

        for key in  operation:
            if key in ('intro','department'):
                continue
            operation[key]=json.dumps(operation[key],ensure_ascii=False)

        item["name"] = StrFunc().str_format(name)
        item['operation']=operation
        item['classify'] = 'operation'

        yield item

  

