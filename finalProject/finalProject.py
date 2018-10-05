from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

########## Import CRUD operations ##########
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

########## Connect to database ##########
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine 
DBSession = sessionmaker(bind = engine)  
session = DBSession()

########## Make an API Endpoint (GET request) ##########
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant)   
    return jsonify(Restorants=[r.serializeRestaurants for r in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return jsonify(RestorantMenu=[i.serializeMenu for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuItemJSON(restaurant_id, menu_id):    
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    return jsonify(MenuItem= item.serializeMenu)

########## Route to different location ##########
##### View restaurants #####
@app.route('/')                                     
@app.route('/restaurants/')     
def showRestaurants():
    restaurants = session.query(Restaurant)   
    return render_template('restaurants.html', restaurants = restaurants)

##### Create new restaurant #####                            
@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash('New restaurant created')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')    
    

##### Edite restaurant #####                            
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id): 
    editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':        
        editedRestaurant.name = request.form['name']  
        session.add(editedRestaurant)
        session.commit()
        flash('Restaurant successfully edited')
        return redirect(url_for('showRestaurants'))
    else:        
        return render_template('editRestaurant.html', restaurant_id = restaurant_id, restaurant = editedRestaurant)   

##### Delete restaurant #####
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':  
        session.delete(deletedRestaurant)
        session.commit()
        flash('Restaurant successfully deleted')
        return redirect(url_for('showRestaurants'))
    else:        
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, restaurant = deletedRestaurant)        
    

##### View restaurant menu #####                                    
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')      
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items) 
    
##### Create new menu item #####                            
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):    
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New menu item created')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)    

##### Edite menu item #####                            
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id): 
    editedMenuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':    

        if request.form['name']:
            editedMenuItem.name = request.form['name']
        if request.form['description']:
            editedMenuItem.description = request.form['description']
        if request.form['price']:
            editedMenuItem.price = request.form['price']
        if request.form['course']:
            editedMenuItem.course = request.form['course']

        session.add(editedMenuItem)
        session.commit()
        flash('Menu item successfully edited')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:        
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedMenuItem)
    

##### Delete menu item #####
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):     
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':  
        session.delete(deletedItem)
        session.commit()
        flash('Menu item successfully deleted')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:        
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = deletedItem)   
    

########## End of file ##########
if __name__ == '__main__': 
    app.secret_key = 'super_secret_key' 
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)


