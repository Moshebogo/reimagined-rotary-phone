#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/restaurants', methods= ['GET', 'POST'])
def restaurants():
    if request.method == 'GET':
        restaraunts = Restaurant.query.all()
        restaurants_to_dict = [restaurant.to_dict() for restaurant in restaraunts] 
        return make_response(jsonify(restaurants_to_dict), 200)
        
    elif request.method =='POST':
        data = request.get_json()
        new_restaraunt = Restaurant()
        for key in data:
            setattr(new_restaraunt, key, data[key])
        db.session.add(new_restaraunt)
        db.session.commit()
        return make_response(jsonify(new_restaraunt.to_dict()), 201)

@app.route('/restaurants/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    print(restaurant)
    if not restaurant:
        return make_response(jsonify({'error': 'Restaurant not found'}), 400)
    
    elif request.method =='GET':    
        return make_response(jsonify(restaurant.res_and_pizza_to_dict()), 200)
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for key in data:
            setattr(restaurant, key, data[key])
        db.session.add(restaurant)
        db.session.commit() 
        return make_response(jsonify(restaurant.to_dict()), 200)  

    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return make_response(jsonify({'status': 'DELETE successful'}), 200)
        
@app.route('/pizzas', methods = ['GET', 'POST'])
def pizzas():
    if request.method == 'GET':
        pizzas = Pizza.query.all()
        pizzas_to_dict = [pizza.to_dict() for pizza in pizzas]
        return make_response(jsonify(pizzas_to_dict), 200)
    
    elif request.method == 'POST':
        data = request.get_json()
        new_pizza = Pizza()
        for key in data:
            setattr(new_pizza, key, data[key])
        db.session.add(new_pizza)   
        db.session.commit()
        return make_response(jsonify(new_pizza.to_dict()), 201) 
    
@app.route('/restaurant_pizzas', methods = ['GET', 'POST'])
def resaurant_pizzas():
    if request.method == 'GET':
        rest_pizzas = RestaurantPizza.query.all()
        rest_pizzas_to_dict = [rest_pizza.to_dict() for rest_pizza in rest_pizzas]
        return make_response(jsonify(rest_pizzas_to_dict), 200)
        
    elif request.method == 'POST':
        data = request.get_json()
        new_rest_pizza = RestaurantPizza()
        for key in data:
            setattr(new_rest_pizza, key, data[key])
        # checks if that pizza_id exists. If it does, adds it. otherwise, sends error.
        pizza_exists = Pizza.query.get(new_rest_pizza.pizza_id)
        restaurant_exists = Restaurant.query.get(new_rest_pizza.restaurant_id)
        if not pizza_exists or not restaurant_exists:
            return make_response(jsonify({'error': 'pizza / restaurant does not exist, not added to database'}), 400)
        db.session.add(new_rest_pizza)
        db.session.commit()
        return make_response(jsonify(pizza_exists.to_dict()), 201) 

if __name__ == '__main__':
    app.run(port=3000)