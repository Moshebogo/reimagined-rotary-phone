from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'     

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'address': self.address}
        
    def res_and_pizza_to_dict(self):
        pizzas = Pizza.query.all()
        return {'id': self.id,
                'name': self.name,
                'address': self.address,
                'pizzas': [pizza.to_dict() for pizza in RestaurantPizza.query.filter(RestaurantPizza.restaurant_id == self.id).all()]}

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now())

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'ingredients': self.ingredients}

class RestaurantPizza(db.Model):    
    __tablename__ = 'restaurant_pizzas'  

    id            = db.Column(db.Integer, primary_key=True)
    price         = db.Column(db.Integer)
    created_at    = db.Column(db.DateTime, default = db.func.now())
    updated_at    = db.Column(db.DateTime, default = db.func.now())

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id      = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    def to_dict(self):
        return {'id': self.id,
                'price': self.price,
                'pizza_id': self.pizza_id,
                'restaurant_id': self.restaurant_id}
    
    @validates("price")
    def validate_price(self,key,price):
        if not 0 < price < 31:
            raise ValueError("Price out of range")
