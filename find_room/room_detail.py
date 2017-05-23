from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import settings

Base = declarative_base()


class RentalDetail(Base):

    __tablename__ = 'rental_detail'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    url = Column(String(256), nullable=False)
    rent = Column(Integer, nullable=False)
    deposit = Column(String(40))
    rental_method = Column(String(40))
    housing_size = Column(String(60), nullable=False)
    face_floor = Column(String(60), nullable=False)
    locate_detail = Column(String(60), nullable=False)
    locate = Column(String(40))
    release_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now())

    def __init__(self, url, rent, deposit, rental_method, housing_size, face_floor, locate_detail, locate, release_at):
        self.url = url
        self.rent = rent
        self.deposit = deposit
        self.rental_method = rental_method
        self.housing_size = housing_size
        self.face_floor = face_floor
        self.locate_detail = locate_detail
        self.locate = locate
        self.release_at = release_at


class PlaceLocation(Base):

    __tablename__ = 'place_location'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    rental_id = Column(Integer, nullable=False)
    lat = Column(String(15), nullable=False)
    lng = Column(String(15), nullable=False)

    def __init__(self, rental_id, lat, lng):
        self.rental_id = rental_id
        self.lat = lat
        self.lng = lng


DBSession = sessionmaker(bind=settings.engine)
