'''
Author: mfuture@qq.com
Date: 2021-10-14 19:41:40
LastEditTime: 2021-10-14 21:42:46
LastEditors: mfuture@qq.com
Description: 
FilePath: /health39/jbk39/spiders/ipproxy.py
'''
import scrapy
import time

CRAWL_INTERVAL = 0.2  # 睡眠时间，反爬

class IpproxySpider(scrapy.Spider):
    name = 'ipproxy'
 

    # custom_settings = {
    #     "DEFAULT_REQUEST_HEADERS": {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    #     }
    # }



    def start_requests(self):

        for i in range(50):
            time.sleep(CRAWL_INTERVAL)
            print(i)
            url='https://www.kuaidaili.com/free/inha/{}/'.format(i+1)
            yield scrapy.Request(url=url, callback=self.init_parse)

    def init_parse(self, response):

        return

        departments = response.xpath('//div[contains(@class,"lookup_department")]//li[position()>1]/a')
    
        for department in departments:
            pinyin=department.xpath("./@href").extract()[0].split("/")[2] #拼音
            
            url=self.base_url+pinyin+'/'

            yield scrapy.Request(url=url, callback=self.section_parse)

    def parse(self, response):
        pass
