# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from room_detail import DBSession, RentalDetail
import requests
from bs4 import BeautifulSoup
import random
from scrapy.log import logger
from scrapy.http import Request
from scrapy.exceptions import IgnoreRequest


class ProxyMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self):
        self.fetch_proxy_url = 'http://www.xicidaili.com/nn/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        self.ip_list = self.get_ip_list(self.fetch_proxy_url, self.headers)
        self.ip_num = len(self.ip_list)
        self.proxy_index = 0

    def process_request(self, request, spider):
        if self.proxy_index > self.ip_num:
            self.ip_list = self.get_ip_list(self.fetch_proxy_url, self.headers)
            self.proxy_index = 0
            self.ip_num = len(self.ip_list)
        cur_proxy_url = self.ip_list[self.proxy_index]
        request.meta['proxy'] = cur_proxy_url

    def process_response(self, request, response, spider):
        logger.info(request.meta)
        if response.status == 200:
            return response
        elif response.status == 302:
            return request
        else:
            self.proxy_index += 1
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    # 从代理网站获取代理ip
    def get_ip_list(self, url, headers):
        logger.info('start get new proxy ip ...')
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append('http://' + str(tds[1].text + ':' + tds[2].text))
        return ip_list


class FilterMiddleware(object):

    def __init__(self):

        session = DBSession()
        results = session.query(RentalDetail).order_by(RentalDetail.id).all()
        self.url_list = []
        for result in results:
            self.url_list.append(result.url)
        self.url_set = set(self.url_list)

    def process_request(self, request, spider):

        if request.url in self.url_set:
            logger.info('Duplicate url %s' % request.url)
            raise IgnoreRequest('Duplicate url %s' % request.url)
        else:
            logger.info('')
            self.url_set.add(request.url)
            return None
