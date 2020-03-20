# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class JobsparsPipeline(object):
    
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongobase = client.scrapy_pars
    
    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, item, spider):
        
        if spider.name == 'hhpars':
            
            if item['salary'][0] == 'от' and item['salary'][3] != 'до':
                min_salary = item['salary'][1]+item['salary'][2]
                max_salary = None
                currency = '₽'

            elif item['salary'][0] == 'от' and item['salary'][3] == 'до':
                min_salary = item['salary'][1]+item['salary'][2]
                max_salary = item['salary'][4]+item['salary'][5]
                currency = '₽'

            else:
                min_salary = None
                max_salary = None
                currency = None
        elif spider.name == sjparse:
            pass
        
        return item
            