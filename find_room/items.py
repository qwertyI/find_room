# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FindRoomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    rent = scrapy.Field()
    deposit = scrapy.Field()
    rental_method = scrapy.Field()
    housing_size = scrapy.Field()
    face_floor = scrapy.Field()
    locate_detail = scrapy.Field()
    locate = scrapy.Field()
    release_at = scrapy.Field()
