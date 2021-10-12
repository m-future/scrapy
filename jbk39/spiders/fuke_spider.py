import scrapy
import time  # 引入time模块

from jbk39.items import Jbk39Item


class jbk39(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "fuke"  # 定义蜘蛛名

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
    }

    def start_requests(self):
        # 定义爬取的链接
        base_url = 'https://jbk.39.net/bw/fuke_t1/'
        yield scrapy.Request(url=base_url, callback=self.init_parse)

    def init_parse(self, response):

        print('goto init_parse')
        urls = []
        cur = response.xpath(
            '//ul[@class="result_item_dots"]/li/span/a/text()')
        dotlen = len(cur)
        listdata = int(cur[dotlen - 2].extract())  # 翻页数量
        for i in range(listdata):
            # for i in range(1):
            ids = i + 1
            url = 'https://jbk.39.net/bw/fuke_t1_p' + str(ids)
            urls.append(url)
            
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        time.sleep(1)  # 延迟2秒执行
        print('goto parse ')

        links_intro = []
        links_treat = []
        links_diagnosis = []
        names = []

        for sel in response.xpath('//*[@class="result_item_top_l"]'):
            name = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()[0]
            names.append(name)
            links_intro.append(link + 'jbzs')
            links_treat.append(link + 'yyzl')
            links_diagnosis.append(link + 'jb')

        '''
		tmp_links = []
		tmp_links.append('https://jbk.39.net/zgnmb/jbzs/')
		tmp_links.append('https://jbk.39.net/gh/jbzs/')
		tmp_links.append('https://jbk.39.net/zgxjz/jbzs/')
		tmp_links.append('https://jbk.39.net/qtdxnz1/jbzs/')

		tmp_links.append('https://jbk.39.net/szdjx/jbzs/')
		tmp_links.append('https://jbk.39.net/gjjb/jbzs/')
		tmp_links.append('https://jbk.39.net/nxszqxtxjx/jbzs/')
		tmp_links.append('https://jbk.39.net/wylzspxbzs/jbzs/')


		for link in tmp_links:
			yield scrapy.Request(url=link, callback=self.intro_parse)

		
		for link in links_intro:
			yield scrapy.Request(url=link, callback=self.intro_parse)
		
		for link in links_treat:
			yield scrapy.Request(url=link, callback=self.treat_parse)
		
		'''
        for link in links_diagnosis:
            yield scrapy.Request(url=link, callback=self.diagnosis_parse)
        '''
		link = 'https://jbk.39.net/zgjl/jbzs'
		yield scrapy.Request(url=link, callback=self.intro_parse)
		link = 'https://jbk.39.net/mjxydy/yyzl'
		yield scrapy.Request(url=link, callback=self.treat_parse)
		
		link = 'https://jbk.39.net/mjxydy/jb'
		yield scrapy.Request(url=link, callback=self.diagnosis_parse)
		'''

    def intro_parse(self, response):

        item = Jbk39Item()

        time.sleep(3)  # 延迟3秒执行
        print('goto intro_parse ')
        name = response.xpath('//div[@class="disease"]/h1/text()').extract()
        intro = response.xpath('//p[@class="introduction"]/text()').extract()
        txt = response.xpath(
            '//span[@class="disease_basic_txt"]/text()').extract()
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

        time.sleep(3)  # 延迟3秒执行
        print('goto treat_parse')

        item = Jbk39Item()

        name = response.xpath('//div[@class="disease"]/h1/text()').extract()

        common_treat = []
        chinese_med_treat = []
        flag = 1  # 1、西医治疗； 2、中医治疗
        text_lists = response.xpath(
            '//p[@class="article_name"]/text() | //p[@class="article_content_text"]/text()').extract()

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

    def diagnosis_parse(self, response):

        time.sleep(1)  # 延迟3秒执行
        print('goto diagnosis_parse')
        item = Jbk39Item()
        name = response.xpath('//div[@class="disease"]/h1/text()').extract()
        diagnosis = []
        identify = []

        #text_lists = response.xpath('//p[@class="article_name"]/text() | //p[@class="article_content_text"]/text()').extract()
        text_lists_diagnosis = response.xpath(
            '//div[@class="art-box"]/p/text() | //div[@class="art-box"]/p/*/text() ').extract()
        text_lists_identify = response.xpath(
            '//div[@class="article_paragraph"]/p/text() | //div[@class="article_paragraph"]/p/*/text() ').extract()
        count1 = 0
        count2 = 0

        for text in text_lists_diagnosis:

            mystr = str(text.replace(u'\u3000', u''))
            count2 = count2 + 1

            diagnosis.append(mystr)

        for text in text_lists_identify:

            mystr = str(text.replace(u'\u3000', u''))
            count1 = count1 + 1
            identify.append(mystr)

        item["diagnosis"] = diagnosis
        item["identify"] = identify
        item["name"] = name
        item['department'] = '妇科'
        item['classify'] = 'diagnosis'

        yield item
