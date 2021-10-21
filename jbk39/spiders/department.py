'''
Author: mfuture@qq.com
Date: 2021-10-13 22:46:09
LastEditTime: 2021-10-16 12:56:55
LastEditors: mfuture@qq.com
Description: 预先爬取各科室并存储，语句解释可参考 disease 爬虫
'''
from pymysql import NULL
import scrapy
import time
from jbk39.items import Jbk39Item

CRAWL_INTERVAL = 0.2  # 睡眠时间，反爬


class SectionSpider(scrapy.Spider):
    name = 'department'

    def __init__(self):
        self.base_url = 'https://jbk.39.net/bw/'

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.init_parse)

    def init_parse(self, response):

        departments = response.xpath(
            '//div[contains(@class,"lookup_department")]//li[position()>1]/a')

        for department in departments:
            pinyin = department.xpath(
                "./@href").extract()[0].split("/")[2]  # 拼音

            url = self.base_url+pinyin+'/'

            yield scrapy.Request(url=url, callback=self.section_parse)

    def section_parse(self, response):

        time.sleep(CRAWL_INTERVAL)

        item = Jbk39Item()

        parent = response.xpath(
            '//div[contains(@class,"lookup_department")]//li[@class="active"]/a')  # 父部门

        pinyin_parent = parent.xpath(
            './@href').extract()[0].split("/")[2]  # 拼音

        chinese_name = parent.xpath('./text()').extract()[0]  # 中文名

        item["department"] = {"pinyin": pinyin_parent,
                              "chinese_name": chinese_name, "parent": "NULL"}

        yield item

        children = response.xpath(
            '//ul[contains(@class,"type_subscreen_unit")]/li/a')  # 子部门

        for child in children:
            pinyin_child = child.xpath(
                './@href').extract()[0].split("/")[2]  # 拼音
            chinese_name = child.xpath('./text()').extract()[0]  # 中文名
            item["department"] = {
                "pinyin": pinyin_child, "chinese_name": chinese_name, "parent": pinyin_parent}
            item["classify"] = 'department'
            yield item
