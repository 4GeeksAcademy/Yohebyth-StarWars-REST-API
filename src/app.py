"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Fav_Planet, Fav_People
#from models import Person

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

@app.route('/user', methods=['GET'])
def handle_get_users():

    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))

    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def handle_get_user(id):
    
    user = User.query.get(id)
    user = user.serialize()

    return jsonify(user), 200

@app.route('/user', methods=['POST'])
def handle_add_user():
    body = request.get_json()

    if 'name' not in body:
        return jsonify({'msj': 'Error. Name not empty'}), 400
    
    if 'email' not in body:
        return jsonify({'msj': 'Error. email not empty'}), 400
    
    if 'password' not in body:
        return jsonify({'msj': 'Error. password not empty'}), 400
    
    exist = User.query.filter_by(email = body["email"]).first()
    if exist: 
       return jsonify ({"msg":"User already exists"})
    
    new_user = User()
    new_user.email = body['email']
    new_user.name = body['name']
    new_user.password= body['password']

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route('/user/<int:id>', methods=['DELETE'])
def habndle_delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg': 'id not exist'}), 404
    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "Deleted user"}), 204

@app.route('/planet', methods=['GET'])
def handle_get_planets():

    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))

    return jsonify(all_planets), 200

@app.route('/planet/<int:id>', methods=['GET'])
def handle_get_planet(id):
    
    planet = Planet.query.get(id)
    planet = planet.serialize()

    return jsonify(planet), 200

@app.route('/people', methods=['GET'])
def handle_get_peoples():

    all_peoples = People.query.all()
    all_peoples = list(map(lambda x: x.serialize(), all_peoples))

    return jsonify(all_peoples), 200

@app.route('/people/<int:id>', methods=['GET'])
def handle_get_people(id):
    
    people = People.query.get(id)
    people = people.serialize()

    return jsonify(people), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
