# encoding=utf-8
from bs4 import BeautifulSoup
import requests
import random
from room_detail import DBSession, RentalDetail, PlaceLocation

# session = DBSession()
#
# results = session.query(RentalDetail).order_by(RentalDetail.id).all()
#
# for result in results:
#     print result.url

a = [1, 2, 3, 4, 5, 6, 1, 3, 5]
b = set(a)
print b
for i in b:
    print i
print 1 in b
print 7 in b
b.add(7)
print 7 in b


