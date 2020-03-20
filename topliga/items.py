# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class TopligaItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    goods_link = scrapy.Field()
    goods_name = scrapy.Field()
    goods_price = scrapy.Field()
    goods_status = scrapy.Field()
    goods_art = scrapy.Field()
    images = scrapy.Field()
    goods_type = scrapy.Field()
