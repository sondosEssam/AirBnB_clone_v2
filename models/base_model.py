#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""


import uuid
from datetime import datetime as d
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String,  Integer, DateTime
import models
if models.typew == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if models.typew == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, nullable=False,
                            default=d.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=d.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = d.now()
            self.updated_at = d.now()
        else:
            if kwargs.get('updated_at') is None:
                self.id = str(uuid.uuid4())
                self.created_at = d.now()
                self.updated_at = d.now()
                for key, val in kwargs.items():
                    if key != "updated_at" and key != "created_at":
                        setattr(self, key, val)
            else:
                kwargs['updated_at'] = d.strptime(kwargs['updated_at'],
                                                  '%Y-%m-%dT%H:%M:%S.%f')
                kwargs['created_at'] = d.strptime(kwargs['created_at'],
                                                  '%Y-%m-%dT%H:%M:%S.%f')
                del kwargs['__class__']
                self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = d.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if dictionary.get("_sa_instance_state") is not None:
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """delt current instince """
        from models import storage
        storage.delete(self)
