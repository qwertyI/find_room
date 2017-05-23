# -*- coding: utf-8 -*-
from room_detail import DBSession, RentalDetail, PlaceLocation
from settings import engine
from scrapy.exceptions import DropItem
from scrapy.log import logger
import functools
import requests
import json
# from redis import Redis
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


def check_spider_pipeline(process_item_method):
    """该注解用在pipeline上
    :param process_item_method:
    :return:
    """

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        # message template for debugging
        msg = " {0} pipeline step".format(self.__class__.__name__)

        # if class is in the spider"s pipeline, then use the
        # process_item method normally.
        if self.__class__ in spider.pipeline:
            logger.info(msg.format("executing"))
            return process_item_method(self, item, spider)

        # otherwise, just return the untouched item (skip this step in
        # the pipeline)
        else:
            logger.info(msg.format("skipping"))
            return item

    return wrapper


# class ItemPipeline(object):
#
#     def __init__(self):
#         session = DBSession()
#         results = session.query(RentalDetail).order_by(RentalDetail.id).all()
#         self.url_list = []
#         for result in results:
#             self.url_list.append(result.url)
#         self.url_set = set(self.url_list)
#
#     @check_spider_pipeline
#     def process_item(self, item, spider):
#         if item['url'] in self.url_set:
#             raise DropItem('Duplicate item found: %s' % item)
#         else:
#             self.url_set.add(item['url'])
#             return item


class FindRoomPipeline(object):

    def __init__(self):
        self.session = DBSession()

    @check_spider_pipeline
    def process_item(self, item, spider):

        rd = RentalDetail(url=item['url'], rent=item['rent'], deposit=item['deposit'],
                          rental_method=item['rental_method'],
                          housing_size=item['housing_size'], face_floor=item['face_floor'],
                          locate_detail=item['locate_detail'], locate=item['locate'],
                          release_at=item['release_at'])

        try:
            print 'start write in database'
            self.session.add(rd)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return item


class TakeLocatePipeline(object):

    def __init__(self):
        self.session = DBSession()
        self.url = 'http://api.map.baidu.com/place/v2/search?query={0}&page_size=10&page_num=0&scope=1&region={1}&output=json&ak=H9VNal4gTO6wKz2XjIQpvSWg'
        self.city = '深圳'

    @check_spider_pipeline
    def process_item(self, item, spider):

        rd = self.session.query(RentalDetail).order_by(RentalDetail.id.desc()).first()
        response = requests.get(self.url.format(rd.locate_detail.encode('utf-8').split(',')[0], self.city))
        try:
            lat = json.loads(response.text)['results'][0]['location']['lat']
            lng = json.loads(response.text)['results'][0]['location']['lng']
            pl = PlaceLocation(rental_id=rd.id, lat=str(lat), lng=str(lng))
            print 'start write in database'
            self.session.add(pl)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return item
