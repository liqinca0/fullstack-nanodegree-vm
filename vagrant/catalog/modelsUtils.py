#!/usr/bin/env python

# Database model helper class
from sqlalchemy.orm.exc import NoResultFound
from models import Category, Item, User


def getCatalogJSON(session):
    '''Retrieve the entire catalog from database and
       return it as a single json object.'''
    categoriesJSON = []

    categories = session.query(Category).all()
    for category in categories:
        items = session.query(Item).filter_by(cat_id=category.id).all()
        categoryJSON = category.serialize
        categoryJSON['Item'] = [item.serialize for item in items]
        categoriesJSON.append(categoryJSON)

    return categoriesJSON


def getUserID(session, email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None


def getUserInfo(session, user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except NoResultFound:
        return None


def createUser(session, login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id
