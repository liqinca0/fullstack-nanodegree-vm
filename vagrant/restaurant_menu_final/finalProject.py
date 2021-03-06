#!/usr/bin/env python

from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine))

#Fake Restaurants
#restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
#restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
#items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
#item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.teardown_request
def remove_session(ex=None):
    session.remove()

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)

@app.route('/restaurant/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    # return "This page will show all my restaurants
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        # return "This page will be for making a new restaurant"
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if editRestaurant and request.form['name']:
            editRestaurant.name = request.form['name']
            session.add(editRestaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
    else:
        # return "This page will be for editing restaurant"
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=editRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    deleteRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if deleteRestaurant:
            session.delete(deleteRestaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
    else:
        # return "This page will be for deleting restaurant"
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=deleteRestaurant)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    if not items:
        flash('You currently do not have any menu items.')   

    return render_template('menu.html', restaurant_id=restaurant_id, restaurant=restaurant, items=items)
    
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course'],
            restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('Created a new menu item {}'.format(newItem.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['name']
        if request.form['price']:
            editItem.price = request.form['price']
        if request.form['course']:
            editItem.course = request.form['course']
        session.add(editItem)
        session.commit()
        flash('Edited menu item {}'.format(editItem.name)) 
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash('Deleted menu item {}'.format(deleteItem.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deleteItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
