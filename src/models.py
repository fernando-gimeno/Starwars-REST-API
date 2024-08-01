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
            "is_active": self.is_active,
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
    mass = db.Column(db.Float, nullable=True)
    hair_color = db.Column(db.String(200), nullable=True)
    skin_color = db.Column(db.String(200), nullable=True)
    eye_color = db.Column(db.String(200), nullable=True)
    birth_year = db.Column(db.String(200), nullable=True)
    
    
    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year
        }
        
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    terrain = db.Column(db.String(200), nullable=True)
    climate = db.Column(db.String(200), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.String(200), nullable=True)
    diameter = db.Column(db.Integer, nullable=True)
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    
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
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "surface_water": self.surface_water
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    model = db.Column(db.String(200), nullable=True)
    vehicle_class = db.Column(db.String(200), nullable=True)
    manufacturer = db.Column(db.String(200), nullable=True)
    cost_in_credits = db.Column(db.String(200), nullable=True)
    length = db.Column(db.String(50), nullable=True)
    crew = db.Column(db.String(50), nullable=True)
    passengers = db.Column(db.String(50), nullable=True)
    max_atmosphering_speed = db.Column(db.String(50), nullable=True)
    cargo_capacity = db.Column(db.String(50), nullable=True)
    consumables = db.Column(db.String(50), nullable=True)
    capacity = db.Column(db.Float, nullable=True)
    
    
    def __repr__(self):
        return '<Vehicle %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "capacity": self.capacity
        }