# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from JP.items import JpItem


class JpPipeline(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.scrapy_pars

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]

        salary = item['salary'].split()

        if spider.name == 'hhru':

            if salary[0] == 'от' and salary[3] != 'до':
                min_salary = salary[1] + salary[2]
                max_salary = None
                currency = '₽'

            elif salary[0] == 'от' and salary[3] == 'до':
                min_salary = salary[1] + salary[2]
                max_salary = salary[4] + salary[5]
                currency = '₽'

            elif salary[0] == 'до':
                max_salary = salary[1] + salary[2]
                min_salary = None
                currency = '₽'

            else:
                min_salary = None
                max_salary = None
                currency = None

        elif spider.name == 'sjru':


            if salary[0] == 'от' and salary[3] != 'до':
                min_salary = salary[1] + salary[2]
                max_salary = None
                currency = salary[3]

            elif salary[0] == 'от' and salary[3] == 'до':
                min_salary = salary[1] + salary[2]
                max_salary = salary[4] + salary[5]
                currency = salary[6]

            elif salary[0] == 'до':
                max_salary = salary[1] + salary[2]
                min_salary = None
                currency = salary[3]

            elif salary[2] == '-':
                min_salary = salary[0] + salary[1]
                max_salary = salary[3] + salary[4]
                currency = salary[5]

            else:
                min_salary = None
                max_salary = None
                currency = None

        jobs_dict = {'source': item['source'],
                     'vac_url': item['vac_link'],
                     'vac_name': item['vac_name'],
                     'salary': item['salary'],
                     'min_salary': min_salary,
                     'max_salary': max_salary,
                     'currency': currency}

        collection.insert_one(jobs_dict)
        return item

    '''def proc_salary(self, item, spider):

        salary = item['salary'].split()

        if spider.name == 'hhru':

            if salary[0] == 'от' and salary[3] != 'до':
                min_salary = salary[1] + salary[2]
                max_salary = None
                currency = '₽'

            elif salary[0] == 'от' and salary[3] == 'до':
                min_salary = salary[1] + salary[2]
                max_salary = salary[4] + salary[5]
                currency = '₽'

            elif salary[0] == 'до':
                max_salary = salary[1] + salary[2]
                min_salary = None
                currency = '₽'

            else:
                min_salary = None
                max_salary = None
                currency = None

        elif spider.name == 'sjru':

            if salary[0] == 'от' and salary[3] != 'до':
                min_salary = salary[1] + salary[2]
                max_salary = None
                currency = salary[3]

            elif salary[0] == 'от' and salary[3] == 'до':
                min_salary = salary[1] + salary[2]
                max_salary = salary[4] + salary[5]
                currency = salary[6]

            elif salary[0] == 'до':
                max_salary = salary[1] + salary[2]
                min_salary = None
                currency = salary[3]

            elif salary[2] == '-':
                min_salary = salary[0] + salary[1]
                max_salary = salary[3] + salary[4]
                currency = salary[5]

            else:
                min_salary = None
                max_salary = None
                currency = None
                

        yield JpItem(min_salary=min_salary, max_salary=max_salary, currency=currency), item'''
