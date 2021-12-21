#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True,
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False)
                      )
"""The association table for Place and Amenity"""


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(
            String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(
            String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longtitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False, backref='place_amenities')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            ''' returns list of review instances with place_id
                equals to the cyrrent Place.id
                FileStorage relationship between Place and Review
            '''
            from models import storage
            all_revs = storage.all(Review)
            lst = []
            for rev in all_revs.values():
                if rev.place_id == self.id:
                    lst.append(rev)
            return lst

        @property
        def amenities(self):
            ''' returns the list of Amenity instances
                based on the attribute amenity_ids that
                contains all Amenity.id linked to the Place
            '''
            from models import storage
            lst = []
            for value in storage.all(Amenity).values():
                if value.id in self.amenity_ids:
                    lst.append(value)
            return lst

        @amenities.setter
        def amenities(self, obj):
            ''' method for adding an Amenity.id to the
                attribute amenity_ids. accepts only Amenity
                objects
            '''
            if type(obj) is Amenity:
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
