'''
Author: mfuture@qq.com
Date: 2021-10-14 19:41:40
LastEditTime: 2021-10-15 00:07:39
LastEditors: mfuture@qq.com
Description: 
FilePath: /health39/jbk39/spiders/ipproxy.py
'''
import scrapy
from jbk39.items import Jbk39Item

class IpproxySpider(scrapy.Spider):
    name = 'ipproxy'

    custom_settings = {
        "RANDOM_DELAY": 3
    }

    def start_requests(self):

        for i in range(5):     
            url='http://www.feidudaili.com/index/gratis/index?page={}'.format(i+1)
            yield scrapy.Request(url=url, callback=self.init_parse)

    def init_parse(self, response):

        item = Jbk39Item()

        ips_list = response.xpath('//tbody/tr')

        for ip_list in ips_list:

            ipproxy=ip_list.xpath('./td/text()').extract()

            item['ipproxy']={"ip":ipproxy[0],"port":ipproxy[1]}
            item['classify']='ipproxy'
            yield item

    def parse(self, response):
        pass
