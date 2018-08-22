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

veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
for vb in veggieBurgers:
    print vb.id
    print vb.price
    print vb.restaurant.name
    print('')

UrbanVeggieBurger = session.query(MenuItem).filter_by(id=10).one()
print('Urban Veggie Burger Price: {}'.format(UrbanVeggieBurger.price))

UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

UrbanVeggieBurger = session.query(MenuItem).filter_by(id=10).one()
print('Urban Veggie Burger Price: {}'.format(UrbanVeggieBurger.price))

veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
for vb in veggieBurgers:
    if vb.price != '$5.99':
        vb.price = '$5.99'
        session.add(vb)
        session.commit()

veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
for vb in veggieBurgers:
    print vb.id
    print vb.price
    print vb.restaurant.name
    print('')