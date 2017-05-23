# coding=utf-8
from scrapy import spiders
from scrapy.http import Request
from find_room.items import FindRoomItem
from find_room import pipelines
import time
from bs4 import BeautifulSoup
import requests
import random


class FiveEightSpider(spiders.Spider):

    name = 'five_eight'
    start_urls = ['http://sz.58.com/chuzu/0/']

    pipeline = set([pipelines.FindRoomPipeline, pipelines.TakeLocatePipeline])

    def parse(self, response):

        if len(self.start_urls) < 10:
            self.start_urls.append(response.xpath('//a[contains(@class, "next")]/@href').extract()[0])
            for sel in response.xpath('//div[contains(@class, "des")]'):
                yield Request(sel.xpath('h2/a/@href').extract()[0], callback=self.rent_detail)
            yield Request(response.xpath('//a[contains(@class, "next")]/@href').extract()[0], callback=self.parse,
                          dont_filter=True)

    def rent_detail(self, response):
        if response.status == 200:
            fri = FindRoomItem()
            sel = response
            fri['url'] = response.url
            fri['rent'] = sel.xpath('//b[contains(@class, "f36")]/text()').extract()[0]
            deposit_list = sel.xpath('//span[contains(@class, "c_333")]/text()').extract()
            fri['deposit'] = deposit_list[0] if len(deposit_list) > 0 else '暂无信息'
            fri['rental_method'] = sel.xpath('//div/div/ul/li[1]/span[2]/text()').extract()[0]
            fri['housing_size'] = sel.xpath('//div/div/ul/li[2]/span[2]/text()').extract()[0].replace(' ', '')
            fri['face_floor'] = sel.xpath('//div/div/ul/li[3]/span[2]/text()').extract()[0]
            fri['locate_detail'] = sel.xpath('//div/div/ul/li[4]/span[2]/a/text()').extract()[0]
            fri['locate'] = sel.xpath('//div/div/ul/li[5]/span[2]/a/text()').extract()[0]
            fri['release_at'] = sel.xpath('//p[contains(@class, "house-update-info")]/text()').extract()[0]
            yield fri

