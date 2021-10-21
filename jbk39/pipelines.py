'''
Author: mfuture@qq.com
Date: 2021-04-22 14:28:08
Description:
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from jbk39.lib.service import DatabaseService as db


class Jbk39Pipeline(object):

    def open_spider(self, spider):
        print('open_spider')
        # 将数据写入文件，以便查看其特征
        self.f = open('data/scrapyItem.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 写入文件，便于观察
        if spider.settings.get("WRITE_SCRAPY_ITEM"):
            try:
                self.f.write(json.dumps(dict(item), ensure_ascii=False))
                self.f.write('\n')
            except Exception as e:
                print(e)

        # 写入数据库保存

        pipelines={
            # 疾病
            "disease:diagnosis": db.create_disease_diagnosis ,
            "disease:treat": db.update_disease_treat,
            "disease:intro": db.update_disease_intro,
            "disease:symptom": db.update_disease_symptom,
            "disease:cause": db.update_disease_cause,

            # 症状
            "symptom:intro": db.create_symptom,
            "symptom:cause": db.update_symptom_cause,
            "symptom:diagnosis": db.update_symptom_diagnosis,
            "symptom:identify": db.update_symptom_identify,
            "symptom:treat_guide": db.update_symptom_treat_guide,

            # 检查鉴别
            "identify": db.create_identify,

            # 手术
            "operation": db.create_operation,

            # 科室
            "department": db.create_department,

            # IP代理
            "ipproxy": db.create_ipproxy,
        }

        pipelines[item['classify']](item)

        return item

    def close_spider(self, spider):
        print('close_spider')
        self.f.close()
