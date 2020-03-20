# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from JP.items import JpItem
from bs4 import BeautifulSoup as bs


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=%D1%82%D0%B0%D0%BA%D1%81%D0%B8']

    def parse(self, response: HtmlResponse):
        next_page = response.css('div._3QBXO div._3R0rZ:nth-child(1) div._1X8YL div._1XEGw div.iJCa5._1JhPh._2gFpt._1znz6._1LlO2._2nteL div._3Qutk div._1Ttd8._2CsQi:nth-child(1) div.L1p51:nth-child(7) > a.icMQ_._1_Cht._3ze9n.f-test-button-dalshe.f-test-link-Dalshe:nth-child(9)::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css('div.f-test-vacancy-item a::attr(href)').extract()
        for vac in vacancy:
            yield response.follow(vac, callback=self.vac_parse)

    def vac_parse(self, response: HtmlResponse):
        res = bs(response.text, 'lxml')
        source = self.allowed_domains[0]
        vac_link = response.url
        vac_name = res.find('h1',{'class':'_3mfro'}).getText()
        salary = res.find('span',{'class':'ZON4b'}).getText()
        yield JpItem(source=source, vac_link=vac_link, vac_name=vac_name, salary=salary)
