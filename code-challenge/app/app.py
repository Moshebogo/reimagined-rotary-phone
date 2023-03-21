#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# home route
@app.route('/')
def home():
    return ''
# route for all restaraunts
@app.route('/restaurants', methods = ['GET'])
def restaurants():
    
    if request.method == 'GET':
        restaurants = Restaurant.query.all()
        rests_to_dicts = [rest.to_dict() for rest in restaurants]
        return make_response(jsonify(rests_to_dicts), 200)
    
#  route for all pizzas
@app.route("/pizzas", methods = ['GET', 'POST'])
def pizzas():
    
    if request.method == 'GET':
        pizzas = Pizza.query.all()
        return make_response(jsonify([pizza.to_dict() for pizza in pizzas]), 200)

    elif request.method =='POST':
        data = request.get_json()
        new_pizza = Pizza()
        for key in data:
            setattr(new_pizza, key, data[key])
            db.session.add(new_pizza)
            db.session.commit()
        return make_response(jsonify(new_pizza.to_dict()), 201)    