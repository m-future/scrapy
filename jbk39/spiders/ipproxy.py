'''
Author: mfuture@qq.com
Date: 2021-10-14 19:41:40
LastEditTime: 2021-10-16 19:17:29
LastEditors: mfuture@qq.com
Description: 从网络第三方获取免费代理ip
FilePath: /health39/jbk39/spiders/ipproxy.py
'''
import scrapy
from jbk39.items import Jbk39Item

class IpproxySpider(scrapy.Spider):
    name = 'ipproxy'

    custom_settings = {
        "DOWNLOAD_DELAY": 0.2,
        "CONCURRENT_REQUESTS_PER_IP" : 1

    }

    def start_requests(self):

        for i in range(1,500): 
            print(i)    
            url='http://www.feidudaili.com/index/gratis/index?page={}'.format(i+1) # 飞度代理
            url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i+1) # 快代理
            yield scrapy.Request(url=url, callback=self.init_parse)

    def init_parse(self, response):

        item = Jbk39Item()

        ips_list = response.xpath('//tbody/tr')

        for ip_list in ips_list:

            ipproxy=ip_list.xpath('./td/text()').extract()
            # item['ipproxy']={"ip":ipproxy[0],"port":ipproxy[1],"speed":int(1000*float(ipproxy[4]))} # 飞度代理
            item['ipproxy']={"ip":ipproxy[0],"port":ipproxy[1],"speed":int(1000*float(ipproxy[5].replace(u'秒','')))} # 快代理

            item['classify']='ipproxy'
            yield item

    def parse(self, response):
        pass
