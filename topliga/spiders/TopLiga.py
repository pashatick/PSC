# -*- coding: utf-8 -*-
from typing import List, Any

import scrapy
from scrapy.http import HtmlResponse
from topliga.items import TopligaItem
from scrapy.loader import ItemLoader


class TopligaSpider(scrapy.Spider):
    name = 'TopLiga'
    allowed_domains = ['topliga.ru']
    start_urls = ['https://topliga.ru/']

    def __init__(self, brand):
        super(TopligaSpider).__init__()
        self.start_urls = [f'https://topliga.ru/brands/{brand}/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@id="navigation_1_next_page"]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)

        goods_list = response.xpath('//div[@class="t_1 col-lg-3 col-md-3 col-sm-4 col-xs-6"]//div[@class="bxr-element-image"]//a/@href').extract()
        for goods in goods_list:
            yield response.follow(goods, callback=self.goods_parse)

    def goods_parse(self, response: HtmlResponse):
        goods_link = response.url
        goods_name = response.xpath('//h1[@class="product-h1-title"]/text()').extract_first()
        goods_price = response.xpath('//div[@class="bxr-market-item-price bxr-format-price bxr-market-price-without-name"]/div/span/text()').extract_first()
        goods_status = response.xpath('//div[@class="internal"]//a/@data-name').extract_first()
        goods_art = response.xpath('//div[@class="product-article-top"]/text()').extract_first()
        images = response.xpath('//a[@data-rel="gallery"]/@href').extract()
        goods_type = response.xpath('//div[@id="bx_breadcrumb_2"]//a//span/text()').extract_first()
        yield TopligaItem(goods_link=goods_link, goods_name=goods_name, goods_price=goods_price,
                          goods_status=goods_status, goods_art=goods_art, images=images, goods_type=goods_type)

    # loader = ItemLoader(item=TopligaItem(), response=response)
    # loader.add_value('goods_link', response.url)
    # loader.add_css('goods_name', 'h1.product-h1-title::text')
    # loader.add_css('goods_price', 'span.bxr-market-format-price::text')
    # loader.add_css('goods_status', 'div.block_sklad a::attr(data-name)')
    # loader.add_value('goods_brand', brand)
    # loader.add_css('goods_art', 'div.product-article-top::text')
    # loader.add_xpath('images', 'div.slick-track a::attr(href)')
