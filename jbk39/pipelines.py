'''
Author: mfuture@qq.com
Date: 2021-04-22 14:28:08
LastEditTime: 2021-10-16 13:06:50
LastEditors: mfuture@qq.com
Description:
FilePath: /health39/jbk39/pipelines.py
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
            
            # # 将数据写入文件，以便查看其特征
            # self.f = open('data/scrapyItem.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
            # # 写入文件，便于观察
            # try:
            #     self.f.write(json.dumps(dict(item), ensure_ascii=False))
            #     self.f.write('\n')
            # except Exception as e:
            #     print(e)

            # # TODO: 是否能写成类似下面的方式，再结合 filter
            # handle_items={
            #     "diagnosis": db.create_diagnosis("disease",item),
            #     "treat": db.update_treat("disease",item),
            #     "intro": db.update_intro("disease",item),
            #     "symptom": db.update_symptom("disease",item),
            #     "cause": db.update_cause("disease",item),
            #     "ipproxy": db.create_ipproxy(item),
            #     "department": db.create_department(item),
            # }  

            # 写入数据库保存
            if item['classify']=='diagnosis':
                    db.create_diagnosis("disease",item)
            elif item['classify']=='treat':
                    db.update_treat("disease",item)
            elif item['classify']=='intro':
                    db.update_intro("disease",item) 
            elif item['classify'] == 'symptom':
                    db.update_symptom("disease",item)				
            elif item['classify'] == 'cause':
                    db.update_cause("disease",item) 
            elif item['classify'] == 'ipproxy':
                    db.create_ipproxy(item)  
            elif item['classify'] == 'department':
                    db.create_department(item)             
            return item

    def close_spider(self,spider):
            print('close_spider')
            # self.f.close()
