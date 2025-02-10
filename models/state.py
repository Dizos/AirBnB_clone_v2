#!/usr/bin/python3
"""
Contains State class model
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """Representation of state"""
    __tablename__ = 'states'
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                            cascade="all, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """
            Returns the list of City objects from storage linked to the current State
            """
            from models import storage
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
