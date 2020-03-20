# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobpars.item import JobparserI
import scrapy
from scrapy.http import HtmlResponse
from jobspars.item import JobsparsItem


class HhparsSpider(scrapy.Spider):
    name = 'hhpars'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&area=76&enable_snippets=true&salary=&st=searchVacancy&text=Такси&from=suggest_post']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('.//a/@href')[0]
        yield response.follow(next_page,callback=self.parse)
                                   
        vacancy = response.xpath('.//a/@href')[0]
        
        for vac_link in vacancy:
            yield response.follow(vac_link, callback=self.vac_parse)
    
    def vac_parse(self, response: HtmlResponse):
        source = self.llowed_domains[0]
        vac_url = self.start_urls
        vac_name = response.xpath('.//h1/text()')
        salary = response.xpath('.//div[@class="vacancy-title"]/p/text()')
        yield JobsparsItem(source=source, vac_url=vac_url, vac_name=vac_name, salary=salary)