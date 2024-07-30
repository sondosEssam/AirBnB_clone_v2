#!/usr/bin/python3
"""
db engine
"""
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """
    data base stroge class
    """
    __engine = None
    __session = None

    def __init__(self):
        """init for engine"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HB_MYSQL_DB), pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """all method to bring all the values inside the engine"""
        new_dict = {}
        for clss in classes:
            if cls is None or str(cls) == classes[clss].__name__:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """new entiity to the table"""
        self.__session.add(obj)

    def save(self):
        """commit changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delte object"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reload prev"""
        Base.metadata.create_all(self.__engine)
        Ses = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Ses)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
