#!/usr/bin/env python

# Database model helper class
from models import Category, Item, User

# Retrieve the entire catalog from database and return it as a single json object.
def getCatalogJSON(session):
    categoriesJSON = []

    try:
        categories = session.query(Category).all()
        for category in categories:
            items = session.query(Item).filter_by(cat_id = category.id).all()
            categoryJSON = category.serialize
            categoryJSON['Item'] = [item.serialize for item in items]
            categoriesJSON.append(categoryJSON)
    except:
        print("ERROR: catalogJSON failed!")

    return categoriesJSON

def getUserID(session, email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def getUserInfo(session, user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def createUser(session, login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id