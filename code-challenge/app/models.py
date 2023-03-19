from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')

    def to_dict(self):
        return {'Id': self.id,
                'name': self.name,
                'address': self.address}

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now())

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')

    def to_dict(self):
        return {'Id': self.id,
                'name': self.name,
                'ingredients': self.ingredients,
                'created_at': self.created_at,
                'updated_at': self.updated_at}

class RestaurantPizza(db.Model):    
    __tablename__ = 'restaurant_pizzas'

    id            = db.Column(db.Integer, primary_key=True)
    price         = db.Column(db.Integer, db.CheckConstraint('price > 1 and price < 30'))
    created_at    = db.Column(db.DateTime, default = db.func.now())
    updated_at    = db.Column(db.DateTime, default = db.func.now())

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id      = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    def to_dict(self):
        return {'Id': self.id,
                'price': self.price,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'restaurant_id': self.restaurant_id,
                'pizza_id': self.pizza_id}