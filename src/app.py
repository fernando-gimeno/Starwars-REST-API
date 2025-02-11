"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from datetime import timedelta
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, Vehicle, Planet, People

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    
    list_of_users = list(map(lambda x: x.serialize(), all_users))

    return jsonify(list_of_users), 200

@app.route('/users', methods=['POST'])
def create_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    if email is None or password is None:
        raise APIException("You need to provide an email and a password", 400)
    
    if len(password) < 6:
        raise APIException("Your password must be greater than 6 characters", 400)
    
    user_exist = User.query.filter_by(email=email).first()
    
    if user_exist is not None:
        raise APIException("User already exist", 400)
    
    user = User(email=email, password=password, is_active=True)
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.serialize()), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    
    if user is None:
        raise APIException(f"User with id #{user_id} not exist in database", 404)
    
    return jsonify(user.serialize()), 200

# Show current user favorites
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    
    if user is None:
        raise APIException(f"User with id #{user_id} not exist in database", 404)
    
    user_favorites = Favorite.query.filter_by(user_id=user_id).first()
    
    if user_favorites is None:
        raise APIException("User has no favorites", 404)
    
    return jsonify(user_favorites.serialize()), 200

# Add people to current user favorites
@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):
    user = User.query.get(user_id)
    
    if user is None:
        raise APIException(f"User with id #{user_id} not exist in database", 404)
    
    people_to_add = People.query.get(people_id)
    
    if people_to_add is None:
        raise APIException(f"People with id #{people_id} not exist in database", 404)
    
    user_favorites = Favorite.query.filter_by(user_id=user_id).first()
    
    if user_favorites is None:
        user_favorites = Favorite(user_id=user_id)
        db.session.add(user_favorites)
    
    if people_to_add in user_favorites.people:
        raise APIException(f"People with id #{people_id} is already in user favorites", 400)
    
    user_favorites.people.append(people_to_add)
    db.session.commit()
    
    return jsonify(user_favorites.serialize()), 201

# Delete people from current user favorites
@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    user = User.query.get(user_id)
    
    if user is None:
        raise APIException(f"User with id #{user_id} not exist in database", 404)
    
    people_to_remove = People.query.get(people_id)
    
    if people_to_remove is None:
        raise APIException(f"People with id #{people_id} not exist in database", 404)
    
    user_favorites = Favorite.query.filter_by(user_id=user_id).first()
    
    if user_favorites is None:
        raise APIException("User has no favorites", 404)
    
    if people_to_remove not in user_favorites.people:
        raise APIException(f"People with id #{people_id} is not in user favorites", 404)
    
    user_favorites.people.remove(people_to_remove)
    db.session.commit()
    
    return jsonify(user_favorites.serialize()), 200

# Add planet to current user favorites
@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    
    if user is None:
        raise APIException(f"User with id #{user_id} not exist in database", 404)
    
    planet_to_add = Planet.query.get(planet_id)
    
    if planet_to_add is None:
        raise APIException(f"Planet with id #{planet_id} not exist in database", 404)
    
    user_favorites = Favorite.query.filter_by(user_id=user_id).first()
    
    if user_favorites is None:
        user_favorites = Favorite(user_id=user_id)
        db.session.add(user_favorites)
        
    if planet_to_add in user_favorites.planets:
        raise APIException(f"Planet with id #{planet_id} is already in user favorites", 400)
    
    user_favorites.planets.append(planet_to_add)
    db.session.commit()
    
    return jsonify(user_favorites.serialize()), 201

# Delete planet from current user favorites
@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    
    if user is None:
        raise APIException(f"User with id #{user_id} not exist in database", 404)
    
    planet_to_remove = Planet.query.get(planet_id)
    
    if planet_to_remove is None:
        raise APIException(f"Planet with id #{planet_id} not exist in database", 404)
    
    user_favorites = Favorite.query.filter_by(user_id=user_id).first()
    
    if user_favorites is None:
        raise APIException("User has no favorites", 404)
    
    if planet_to_remove not in user_favorites.planets:
        raise APIException(f"Planet with id #{planet_id} is not in user favorites", 404)
    
    user_favorites.planets.remove(planet_to_remove)
    db.session.commit()
    
    return jsonify(user_favorites.serialize()), 200

# Add vehicle to current user favorites
@app.route('/users/<int:user_id>/favorites/vehicles/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(user_id, vehicle_id):
    user = User.query.get(user_id)
    
    if user is None:
        raise APIException(f"User with id #{user_id} not exist in database", 404)
    
    vehicle_to_add = Vehicle.query.get(vehicle_id)
    
    if vehicle_to_add is None:
        raise APIException(f"Vehicle with id #{vehicle_id} not exist in database", 404)
    
    user_favorites = Favorite.query.filter_by(user_id=user_id).first()
    
    if user_favorites is None:
        user_favorites = Favorite(user_id=user_id)
        db.session.add(user_favorites)
        
    if vehicle_to_add in user_favorites.vehicles:
        raise APIException(f"Vehicle with id #{vehicle_id} is already in user favorites", 400)
        
    user_favorites.vehicles.append(vehicle_to_add)
    db.session.commit()
    
    return jsonify(user_favorites.serialize()), 201

# Delete vehicle from current user favorites
@app.route('/users/<int:user_id>/favorites/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(user_id, vehicle_id):
    user = User.query.get(user_id)
    
    if user is None:
        raise APIException(f"User with id #{user_id} not exist in database", 404)
    
    vehicle_to_remove = Vehicle.query.get(vehicle_id)
    
    if vehicle_to_remove is None:
        raise APIException(f"Vehicle with id #{vehicle_id} not exist in database", 404)
    
    user_favorites = Favorite.query.filter_by(user_id=user_id).first()
    
    if user_favorites is None:
        raise APIException("User has no favorites", 404)
    
    if vehicle_to_remove not in user_favorites.vehicles:
        raise APIException(f"Vehicle with id #{vehicle_id} is not in user favorites", 404)
    
    user_favorites.vehicles.remove(vehicle_to_remove)
    db.session.commit()
    
    return jsonify(user_favorites.serialize()), 200

# Get all people
@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    
    list_people = list(map(lambda x: x.serialize(), all_people))
    
    return jsonify(list_people), 200

@app.route('/people', methods=['POST'])
def create_people():
    name = request.json.get('name')
    gender = request.json.get('gender')
    height = request.json.get('height')
    mass = request.json.get('mass')
    hair_color = request.json.get('hair_color')
    skin_color = request.json.get('skin_color')
    eye_color = request.json.get('eye_color')
    birth_year = request.json.get('birth_year')

    # Check if all required fields are present
    if not name or not gender:
        raise APIException("Missing required fields", 400)
    
    # Check if the people already exists in the database
    existing_people = People.query.filter_by(name=name).first()
    if existing_people:
        raise APIException("People already exists", 400)
    
    # Create a new people object
    new_people = People(
        name=name,
        gender=gender,
        height=height,
        mass=mass,
        hair_color=hair_color,
        skin_color=skin_color,
        eye_color=eye_color,
        birth_year=birth_year
    )

    # Add the new people to the database
    db.session.add(new_people)
    db.session.commit()
    
    return jsonify(new_people.serialize()), 201
    
# Get people by people_id
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    people = People.query.get(people_id)
    
    if people is None:
        raise APIException(f"People with id #{people_id} not exist in database", 404)
    
    return jsonify(people.serialize()), 200

# Get all planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planet.query.all()
    
    list_planets = list(map(lambda x: x.serialize(), all_planets))
    
    return jsonify(list_planets), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    name = request.json.get('name')
    terrain = request.json.get('terrain')
    climate = request.json.get('climate')
    population = request.json.get('population')
    gravity = request.json.get('gravity')
    diameter = request.json.get('diameter')
    rotation_period = request.json.get('rotation_period')
    orbital_period = request.json.get('orbital_period')
    surface_water = request.json.get('surface_water')

    # Check if all required fields are present
    if not name:
        raise APIException("Missing required fields", 400)
    
    # Check if the people already exists in the database
    existing_people = Planet.query.filter_by(name=name).first()
    if existing_people:
        raise APIException("Planet already exists", 400)
    
    # Create a new people object
    new_planet = Planet(
        name=name,
        terrain=terrain,
        climate=climate,
        population=population,
        gravity=gravity,
        diameter=diameter,
        rotation_period=rotation_period,
        orbital_period=orbital_period,
        surface_water=surface_water
    )

    # Add the new people to the database
    db.session.add(new_planet)
    db.session.commit()
    
    return jsonify(new_planet.serialize()), 201

# Get planet by planet_id
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    
    if planet is None:
        raise APIException(f"Planet with id #{planet_id} not exist in database", 404)
    
    return jsonify(planet.serialize()), 200

# Get all vehicles
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicle.query.all()
    
    list_vehicles = list(map(lambda x: x.serialize(), all_vehicles))
    
    return jsonify(list_vehicles), 200

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    name = request.json.get('name')
    model = request.json.get('model')
    vehicle_class = request.json.get('vehicle_class')
    manufacturer = request.json.get('manufacturer')
    cost_in_credits = request.json.get('cost_in_credits')
    length = request.json.get('length')
    crew = request.json.get('crew')
    max_atmosphering_speed = request.json.get('max_atmosphering_speed')
    cargo_capacity = request.json.get('cargo_capacity')
    consumables = request.json.get('consumables')

    # Check if all required fields are present
    if not name:
        raise APIException("Missing required fields", 400)
    
    # Check if the people already exists in the database
    existing_people = Vehicle.query.filter_by(name=name).first()
    if existing_people:
        raise APIException("Vehicle already exists", 400)
    
    # Create a new people object
    new_vehicle = Vehicle(
        name=name,
        model=model,
        vehicle_class=vehicle_class,
        manufacturer=manufacturer,
        cost_in_credits=cost_in_credits,
        length=length,
        crew=crew,
        max_atmosphering_speed=max_atmosphering_speed,
        cargo_capacity=cargo_capacity,
        consumables=consumables
    )

    # Add the new people to the database
    db.session.add(new_vehicle)
    db.session.commit()
    
    return jsonify(new_vehicle.serialize()), 201

# Get vehicle by vehicle_id
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    
    if vehicle is None:
        raise APIException(f"Vehicle with id #{vehicle_id} not exist in database", 404)
    
    return jsonify(vehicle.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
