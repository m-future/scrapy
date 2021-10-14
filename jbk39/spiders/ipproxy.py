'''
Author: mfuture@qq.com
Date: 2021-10-14 19:41:40
LastEditTime: 2021-10-14 20:20:38
LastEditors: mfuture@qq.com
Description: 
FilePath: /health39/jbk39/spiders/ipproxy.py
'''
import scrapy
import time

CRAWL_INTERVAL = 2  # 睡眠时间，反爬

class IpproxySpider(scrapy.Spider):
    name = 'ipproxy'
    allowed_domains = ['proxy.com']
    start_urls = ['http://proxy.com/']



    def start_requests(self):

        for i in range(10):
            time.sleep(CRAWL_INTERVAL)
            print(i)
            url='https://www.kuaidaili.com/free/inha/{}/'.format(i+1)
            yield scrapy.Request(url=url, callback=self.init_parse)

    def init_parse(self, response):

        print(response)

        return

        departments = response.xpath('//div[contains(@class,"lookup_department")]//li[position()>1]/a')
    
        for department in departments:
            pinyin=department.xpath("./@href").extract()[0].split("/")[2] #拼音
            
            url=self.base_url+pinyin+'/'

            yield scrapy.Request(url=url, callback=self.section_parse)

    def parse(self, response):
        pass
