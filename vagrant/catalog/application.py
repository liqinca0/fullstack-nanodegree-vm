#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User

#Session oauth login
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response

from modelsUtils import getCatalogJSON, getUserID, createUser
from oauthUtils import require_login, gen_state_token, google_connect, facebook_connect, logout

APPLICATION_NAME = "Vegan Shopping List"
app.jinja_env.globals.update(gen_state_token=gen_state_token)

#Connect to Database and create database session
engine = create_engine('sqlite:///catalogWithOAuth.db')
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine))
Categories = session.query(Category).order_by(asc(Category.name))

def registerUser():
    # New user login, create a new user if the user doesn't exist.
    user_id = getUserID(session, login_session['email'])
    if not user_id:
        user_id = createUser(session, login_session)
    login_session['user_id'] = user_id

    response = make_response(json.dumps("You are now logged in as {}".format(login_session['username'])), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.teardown_request
def remove_session(ex=None):
    session.remove()

# Login with Google oauth api
@app.route('/gconnect', methods=['POST'])
def gconnect():
    response = google_connect(request)
    if response is not None:
        # Login failure or user already logged in.
        return response

    return registerUser()
    
# Login with Facebook oauth api
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    response = facebook_connect(request)
    if response is not None:
        # Login failure or user already logged in.
        return response
    
    return registerUser()

# Logout based on provider
@app.route('/logout')
def showLogout():
    logout()
    return redirect(url_for('showCategories'))

# Logout based on provider
@app.route('/error')
def showError():
    return render_template('error.html', errormsg = "Oops... Something went wrong.  Please check the console and try again.")

#Show home page: categories | latest items
@app.route('/')
def showCategories():
    Categories = session.query(Category).order_by(asc(Category.name))
    latestItems = session.query(Item).order_by(asc(Item.created_date)).limit(Categories.count())
    return render_template('catalog.html',
        leftPanel = 'category/categorylist.html', rightPanel = 'category/latestlist.html',
        categories = Categories,
        latestItems = latestItems)

#Show categories | category items
@app.route('/catalog/<category_name>/items')
def showCategoryItems(category_name):
    category_id = request.args.get('category_id')
    if category_id is None:
        flash("Oops... Category {} is not found".format(category_name))
        return redirect(url_for('showCategories'))
    
    items = session.query(Item).filter_by(cat_id = category_id).order_by(asc(Item.title)).all()
    selectedCategory = session.query(Category).filter_by(id = category_id).one()
    # jsonify(Items=[[item.serialize for item in items]])
    return render_template('catalog.html',
        leftPanel = 'category/categorylist.html', rightPanel = 'category/itemlist.html',
        categories = Categories,
        selectedCategory = selectedCategory,
        items = items)

#Show category item info
@app.route('/catalog/<category_name>/<item_title>')
def showCategoryItem(category_name, item_title):
    item_id = request.args.get('item_id')
    if item_id is None:
        flash("Oops... Item {} is not found".format(item_title))
        return redirect(url_for('showCategories'))
    
    selectedCategoryItem = session.query(Item).filter_by(id = item_id).one()
    if selectedCategoryItem is None:
        flash("Oops... Item {} is not found".format(item_title))
        return redirect(url_for('showCategories'))
    
    items = session.query(Item).filter_by(cat_id = selectedCategoryItem.cat_id).order_by(asc(Item.title)).all()
    return render_template('catalog.html',
        leftPanel = 'category/itemlist.html', rightPanel = 'category/item.html',
        selectedCategory = selectedCategoryItem.category,
        selectedCategoryItem = selectedCategoryItem,
        items = items)

#Add a new catalog/category item
@app.route('/catalog/new', methods=['GET','POST'])
def newCatalogItem():
    require_login()

    if request.method == 'POST':
        if request.form['title']:
            newItem = Item(
                title = request.form['title'],
                description = request.form['description'],
                cat_id = request.form['category'],
                user_id = login_session['user_id'])
            session.add(newItem)
            session.commit()
            flash("{} as been successfully added to {}".format(newItem.title, newItem.category.name))
            return redirect(url_for('showCategoryItem', category_name = newItem.category.name, item_title = newItem.title, item_id = newItem.id))
        else:
            flash("Oops... Failed to create a new item.")
            return redirect(url_for('showCategories'))
    else:
        category_id = request.args.get('category_id')
        if category_id is not None:
            selectedCategory = session.query(Category).filter_by(id = category_id).one()
            return render_template('catalog.html',
                leftPanel = 'category/categorylist.html', rightPanel = 'category/newitem.html',
                categories = Categories,
                selectedCategory = selectedCategory)
        else:
            return render_template('catalog.html',
                leftPanel = 'category/categorylist.html', rightPanel = 'category/newitem.html',
                categories = Categories)

#Edit a category item
@app.route('/catalog/<item_title>/edit', methods=['GET','POST'])
def editCategoryItem(item_title):
    require_login()

    item_id = request.args.get('item_id')
    if item_id is None:
        flash("Oops... Item {} is not found".format(item_title))
        return redirect(url_for('showCategories'))

    editCategoryItem = session.query(Item).filter_by(id = item_id).one()
    if editCategoryItem is None:
        flash("Oops... Item {} is not found".format(item_title))
        return redirect(url_for('showCategories'))

    if request.method == 'POST':
        if request.form['title']:
            editCategoryItem.title = request.form['title']
        if request.form['description']:
            editCategoryItem.description = request.form['description']
        session.add(editCategoryItem)
        session.commit()
        flash("{} as been successfully updated in {}".format(editCategoryItem.title, editCategoryItem.category.name))
        return redirect(url_for('showCategoryItem', category_name = editCategoryItem.category.name, item_title = editCategoryItem.title, item_id = editCategoryItem.id))
    else:
        items = session.query(Item).filter_by(cat_id = editCategoryItem.cat_id).order_by(asc(Item.title)).all()
        return render_template('catalog.html',
            leftPanel = 'category/itemlist.html', rightPanel = 'category/edititem.html',
            selectedCategory = editCategoryItem.category,
            selectedCategoryItem = editCategoryItem,
            items = items)

#Delete a category item
@app.route('/catalog/<item_title>/delete', methods = ['GET','POST'])
def deleteCategoryItem(item_title):
    require_login()

    item_id = request.args.get('item_id')
    if item_id is None:
        flash("Oops... Item {} is not found".format(item_title))
        return redirect(url_for('showCategories'))

    deleteCategoryItem = session.query(Item).filter_by(id = item_id).one()
    if deleteCategoryItem is None:
        flash("Oops... Item {} is not found".format(item_title))
        return redirect(url_for('showCategories'))

    if request.method == 'POST':
        category = deleteCategoryItem.category
        session.delete(deleteCategoryItem)
        session.commit()
        flash("{} as been successfully removed from {}".format(deleteCategoryItem.title, deleteCategoryItem.category.name))
        return redirect(url_for('showCategoryItems', category_name = category.name, category_id = category.id))
    else:
        items = session.query(Item).filter_by(cat_id = deleteCategoryItem.cat_id).order_by(asc(Item.title)).all()
        return render_template('catalog.html',
            leftPanel = 'category/itemlist.html', rightPanel = 'category/deleteitem.html',
            selectedCategory = deleteCategoryItem.category,
            selectedCategoryItem = deleteCategoryItem,
            items = items)

#JSON API to view all catalog items
@app.route('/catalog.json')
def catalogJSON():
    return jsonify(Category=getCatalogJSON(session))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
