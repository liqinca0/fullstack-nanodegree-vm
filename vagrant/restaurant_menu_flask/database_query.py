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

print('Menu Items:')
items = session.query(MenuItem).all()
for item in items:
    print('    {}'.format(item.name))

print('\nRestaurants:')
restaurants = session.query(Restaurant).all()
for rest in restaurants:
    print('    {}'.format(rest.name))
