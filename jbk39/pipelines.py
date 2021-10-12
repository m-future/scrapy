# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class Jbk39Pipeline(object):

	def open_spider(self,spider):
		self.f = open('job2.json','w',encoding='utf-8')

	def process_item(self, item, spider):
		self.f.write(json.dumps(dict(item),ensure_ascii=False))
		self.f.write('\n')
		return item

	def close_spider(self,spider):
		self.f.close()