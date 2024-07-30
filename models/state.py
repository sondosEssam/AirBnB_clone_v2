#!/usr/bin/python3
""" State Module for HBNB project """


from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
import models
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    if models.typew == "db":
        __tablename__ = "states"
        name = Column(String(128),  nullable=False)
        cities = relationship("City", backref="state")
    else:
        @property
        def cities(self):
            from models import storage
            from models.city import City
            """getter"""
            cityy = []
            all_cities = storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    cityy.append(city)
            return cityy
        name = ""
