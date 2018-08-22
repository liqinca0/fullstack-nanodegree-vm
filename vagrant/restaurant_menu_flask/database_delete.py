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

spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
print spinach.restaurant.name

session.delete(spinach)
session.commit()

spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
