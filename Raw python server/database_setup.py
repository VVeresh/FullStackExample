import sys      # for manipulation of Py run-time environment
from sqlalchemy import \
Column, ForeignKey, Integer, String     #  classes for writing mapper code

########## Configuration ##########

from sqlalchemy.ext.declarative import \
declarative_base                        # used for configuration and class code

from sqlalchemy.orm import relationship # for creating foriegn key relationship

from sqlalchemy import create_engine    # for configuration code on the end of file

Base = declarative_base()   # let SQLAlchemy know that they are special classes for SQL Alchemy that correspond to tables in our db

##########  Classes ##########
 # Classes extend Base clase and represent our tables in db
 # Inside each classes we must create table representation with special variable

class Restaurant(Base):
    ##### Tables #####
    __tablename__ = 'restaurant'
    
    name = Column(String(80), nullable = False)     # mapper for columns in table
    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    ##### Tables #####
    __tablename__ = 'menu_item'
    
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    restaurant = relationship(Restaurant)   # connection with Restaurant table

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return{
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course
        }

########## end of file - Configuration ##########

engine = create_engine('sqlite:///restaurantmenu.db')   # point to db we use and create file that we can use for other db like MySQL

Base.metadata.create_all(engine)    # go to db and adds the classes as a new tables in our database