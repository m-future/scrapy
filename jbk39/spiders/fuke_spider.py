import scrapy
import time  # 引入time模块
import logging

from jbk39.items import Jbk39Item

CRAWL_INTERVAL= 0.5 #睡眠时间，防止爬虫被墙


class jbk39(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "fuke"  # 定义蜘蛛名

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
    }

    def start_requests(self):
        # 定义爬取的链接
        base_url = 'https://jbk.39.net/bw/fuke_t1/'  # 疾病
        yield scrapy.Request(url=base_url, callback=self.init_parse)

    def init_parse(self, response):

        print('goto init_parse')
        urls = []  # 全部疾病的分页连接
        cur = response.xpath('//ul[@class="result_item_dots"]/li/span/a/text()')
        dotlen = len(cur)
        listdata = int(cur[dotlen - 2].extract())  # 翻页数量
        for i in range(listdata):
            url = 'https://jbk.39.net/bw/fuke_t1_p' + str(i+1)
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        time.sleep(CRAWL_INTERVAL)  # 延迟2秒执行
        print('goto parse ')

        links_intro = []
        links_treat = []
        links_diagnosis = []

        for sel in response.xpath('//*[@class="result_item_top_l"]'):
            link = sel.xpath('a/@href').extract()[0]
            links_intro.append(link + 'jbzs') #简介
            links_treat.append(link + 'yyzl') #治疗
            links_diagnosis.append(link + 'jb') #鉴别

        '''		
		for link in links_intro:
			yield scrapy.Request(url=link, callback=self.intro_parse)
		
		for link in links_treat:
			yield scrapy.Request(url=link, callback=self.treat_parse)
		
		'''
        for link in links_diagnosis:
            yield scrapy.Request(url=link, callback=self.diagnosis_parse)

    def intro_parse(self, response):

        item = Jbk39Item()

        time.sleep(CRAWL_INTERVAL)  # 延迟3秒执行
        print('goto intro_parse ')
        name = response.xpath('//div[@class="disease"]/h1/text()').extract()
        intro = response.xpath('//p[@class="introduction"]/text()').extract()
        txt = response.xpath('//span[@class="disease_basic_txt"]/text()').extract()
        if (len(txt) > 1):
            alias = txt[1]
        else:
            alias = ''
        item['name'] = name[0]
        item['intro'] = intro[0]
        item['alias'] = alias
        item['department'] = '妇科'
        item['classify'] = 'intro'
        yield item

    def treat_parse(self, response):

        time.sleep(CRAWL_INTERVAL)  # 延迟3秒执行
        print('goto treat_parse')

        item = Jbk39Item()

        name = response.xpath('//div[@class="disease"]/h1/text()').extract()

        common_treat = []
        chinese_med_treat = []
        flag = 1  # 1、西医治疗； 2、中医治疗
        text_lists = response.xpath('//p[@class="article_name"]/text() | //p[@class="article_content_text"]/text()').extract()

        for text in text_lists:

            mystr = str(text.replace(u'\u3000', u''))

            if mystr.find('中医治疗') >= 0:
                flag = 2

            if mystr.find("西医治疗") < 0 and mystr.find("中医治疗") < 0:

                if flag == 1:
                    common_treat.append(mystr)
                else:
                    chinese_med_treat.append(mystr)

        item["common_treat"] = common_treat
        item["chinese_med_treat"] = chinese_med_treat
        item['department'] = '妇科'
        item["name"] = name
        item['classify'] = 'treat'

        yield item

    '''
    description: 诊断
    param {*} self
    param {*} response
    return {*}
    '''
    def diagnosis_parse(self, response):

        time.sleep(CRAWL_INTERVAL)  # 延迟3秒执行
        print('goto diagnosis_parse')
        item = Jbk39Item()
        name = response.xpath('//div[@class="disease"]/h1/text()').extract()
        diagnosis = []
        identify = []

        #text_lists = response.xpath('//p[@class="article_name"]/text() | //p[@class="article_content_text"]/text()').extract()
        text_lists_diagnosis = response.xpath('//div[@class="art-box"]/p/text() | //div[@class="art-box"]/p/*/text() ').extract()
        text_lists_identify = response.xpath('//div[@class="article_paragraph"]/p/text() | //div[@class="article_paragraph"]/p/*/text() ').extract()

        for text in text_lists_diagnosis:

            mystr = str(text.replace(u'\u3000', u''))
            diagnosis.append(mystr)

        for text in text_lists_identify:

            mystr = str(text.replace(u'\u3000', u''))
            identify.append(mystr)

        item["diagnosis"] = diagnosis
        item["identify"] = identify
        item["name"] = name
        item['department'] = '妇科'
        item['classify'] = 'diagnosis'

        yield item
