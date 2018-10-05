########## Setup code ##########

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()

########## Query code ###########

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

"""
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

##### Filter to find entry #####
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()
#print UrbanVeggieBurger.price

##### Update single price #####
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"
"""
##### Update all price #####
for veggieBurger in veggieBurgers:
    if veggieBurger.price != '$2.99':
        veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit()

for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"
