from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_people = db.Table(
    "favorite_people",
    db.Column("favorite_id", db.Integer, db.ForeignKey("favorite.id")),
    db.Column("people_id", db.Integer, db.ForeignKey("people.id"))
)

favorite_planets = db.Table(
    "favorite_planets",
    db.Column("favorite_id", db.Integer, db.ForeignKey("favorite.id")),
    db.Column("planet_id", db.Integer, db.ForeignKey("planet.id"))
)

favorite_vehicles = db.Table(
    "favorite_vehicles",
    db.Column("favorite_id", db.Integer, db.ForeignKey("favorite.id")),
    db.Column("vehicle_id", db.Integer, db.ForeignKey("vehicle.id"))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorite", backref="user", lazy=True, uselist=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": self.favorites.serialize() if self.favorites else list()
        }
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people = db.relationship("People", secondary=favorite_people, backref="favorites")
    planets = db.relationship("Planet", secondary=favorite_planets, backref="favorites")
    vehicles = db.relationship("Vehicle", secondary=favorite_vehicles, backref="favorites")
    
    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "people": list(map(lambda x: x.serialize(), self.people)),
            "planets": list(map(lambda x: x.serialize(), self.planets)),
            "vehicles": list(map(lambda x: x.serialize(), self.vehicles))
        }
        
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    gender = db.Column(db.String(200), nullable=False)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight
        }
        
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    terrain = db.Column(db.String(200), nullable=True)
    climate = db.Column(db.String(200), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.Float, nullable=True)
    diameter = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return '<Planet %r' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            "population": self.population,
            "gravity": self.gravity,
            "diameter": self.diameter
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    model = db.Column(db.String(200), nullable=False)
    manufacturer = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return '<Vehicle %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost": self.cost,
            "capacity": self.capacity
        }