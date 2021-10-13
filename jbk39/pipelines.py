'''
Author: mfuture@qq.com
Date: 2021-04-22 14:28:08
LastEditTime: 2021-10-13 11:37:36
LastEditors: mfuture@qq.com
Description: 
FilePath: /jbk39/jbk39/pipelines.py
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from .lib.db_service import database as db

class Jbk39Pipeline(object):

	def open_spider(self,spider):
    		print('open_spider')
			# self.f = open('example.json','w',encoding='utf-8')

	def process_item(self, item, spider):
			# self.f.write(json.dumps(dict(item),ensure_ascii=False))
			# self.f.write('\n')
			if item['classify']=='diagnosis':
    				db.create_diagnosis("disease",item)
			elif item['classify']=='treat':
    				db.update_treat("disease",item)
			elif item['classify']=='intro':
    				db.create_intro("disease",item)   				
    			
			return item

	def close_spider(self,spider):
    		print('close_spider')
			# self.f.close()