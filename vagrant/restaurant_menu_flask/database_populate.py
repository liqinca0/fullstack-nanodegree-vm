#!/usr/bin/env python

# Configuration
import os
import sys


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

# Bind sqlalchemy classes to database
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Create first restaurant
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
firstRestaurant = session.query(Restaurant).first()
print('First Restaurant: {}'.format(firstRestaurant.name))


# Create first menu item
soycheesepizza = MenuItem(
    name = "Soy Cheese Pie",
    description = "Made with all vegan ingredients and Daiya mozzarella",
    course = "Entree",
    price = "$8.99",
    restaurant = myFirstRestaurant)
session.add(soycheesepizza)
session.commit()
