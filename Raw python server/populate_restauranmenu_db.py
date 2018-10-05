from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')   # let`s our program know which db engine we want to communicate with.

Base.metadata.bind = engine     # make connection between class definition and corresponding tables in db

DBSession = sessionmaker(bind = engine)    # this establishes a link of communication between our code executions and engine we just created

session = DBSession()  # DBSession object give a staging zone for all object that are loaded to him

myFirstRestaurant = Restaurant(name = "Pizza Palace")  # making new entry for db

session.add(myFirstRestaurant)     # add myFirstRestaurant to staging zone
    
session.commit()                   # store to db

session.query(Restaurant).all()    # go to db, find 'Restaurant' table and return all entries as list

cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)

session.add(cheesepizza)

session.commit()

session.query(MenuItem).all()