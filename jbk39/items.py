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
    department = scrapy.Field() # 科室
    diagnosis = scrapy.Field() #诊断
    identify = scrapy.Field() #鉴别
    common_treat = scrapy.Field() #一般治疗
    chinese_med_treat = scrapy.Field() #中医治疗

    pass
