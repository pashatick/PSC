# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from JP.items import JpItem
from bs4 import BeautifulSoup as bs
from lxml import html


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://rostov.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=%D0%A2%D0%B0%D0%BA%D1%81%D0%B8&showClusters=true']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)'
        ).extract()

        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        res = bs(response.text, 'lxml')
        source = self.allowed_domains[0]
        vac_link = response.url
        vac_name = response.css('div.vacancy-title h1.bloko-header-1::text').extract_first()
        salary = res.find('div', {'class':'vacancy-title'}).find('p',{'class':'vacancy-salary'}).find('span').getText()

        yield JpItem(source=source, vac_link=vac_link, vac_name=vac_name, salary=salary)
