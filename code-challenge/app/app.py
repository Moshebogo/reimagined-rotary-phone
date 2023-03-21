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

@app.route('/restaurants', methods = ['GET'])
def restaurants():
    rests = Restaurant.query.all()
    rests_to_dict = [rest.to_dict() for rest in rests]
    return make_response(jsonify(rests_to_dict), 200)

@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurant_by_id(id):
    rest = Restaurant.query.get(id)
    if not rest:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)
    if request.method == 'GET':
        rest_to_dict = rest.with_pizza_to_dict()
        return make_response(jsonify(rest_to_dict), 200)
    
    elif request.method == 'DELETE':
        rps =  RestaurantPizza.query.filter(RestaurantPizza.id == rest.id).all()
        for row in rps:
            db.session.delete(row)
        db.session.delete(rest)
        db.session.commit()
        return make_response(jsonify({"": ""}), 200)
    

@app.route('/pizzas', methods = ['GET'])
def pizzas():
    pizzas = Pizza.query.all()
    pizzas_to_dict = [pizza.to_dict() for pizza in pizzas]  
    return make_response(jsonify(pizzas_to_dict), 200)

@app.route('/restaurant_pizzas', methods = ['POST'])
def restaurant_pizzas():

    if request.method == 'POST':
        data = request.get_json()
        new_rest_and_pizza = RestaurantPizza()
        for key in data:
            setattr(new_rest_and_pizza, key, data[key])
        # check if rest exists, if yes, adds to database. Otherwise, says "that pizza / restaurant does not exist"
        rest_exists = Restaurant.query.get(new_rest_and_pizza.restaurant_id)  
        pizza_exists = Pizza.query.get(new_rest_and_pizza.pizza_id)
        if not rest_exists or not pizza_exists:
            return make_response(jsonify({"error": "that pizza / restaurant does not exist"}), 404)
        # if rest_exists and pizza_exists
        db.session.add(new_rest_and_pizza)
        db.session.commit()
    return make_response(jsonify(pizza_exists.to_dict()), 201)


if __name__ == '__main__':
    app.run(port=5555)