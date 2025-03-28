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
    if not all_users:
        return jsonify({"msg":"Users empty"}),404
    all_users = list(map(lambda x: x.serialize(), all_users))

    return jsonify(all_users), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_get_user(user_id):
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg":"User not exist"}),404
    user = user.serialize()

    return jsonify(user), 200

@app.route('/user', methods=['POST'])
def handle_add_user():
    body = request.get_json()

    if 'name' not in body:
        return jsonify({'msj': 'name is required'}), 400
    
    if 'email' not in body:
        return jsonify({'msj': 'email is required'}), 400
    
    if 'password' not in body:
        return jsonify({'msj': 'password is required'}), 400
    
    user_exist = User.query.filter_by(email = body["email"]).first()
    if user_exist: 
       return jsonify ({"msg":"User already exists"})
    
    new_user = User()
    new_user.email = body['email']
    new_user.name = body['name']
    new_user.password= body['password']

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route('/user/<int:user_id>', methods=['DELETE'])
def habndle_delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'user not exist'}), 404
    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "Deleted user"}), 204

@app.route('/planet', methods=['GET'])
def handle_get_planets():

    all_planets = Planet.query.all()
    if not all_planets:
        return jsonify({"msg":"Planets empty"}),404
    all_planets = list(map(lambda x: x.serialize(), all_planets))

    return jsonify(all_planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def handle_get_planet(planet_id):
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg":"Planet not exist"}),404
    planet = planet.serialize()

    return jsonify(planet), 200

@app.route('/planet', methods=['POST'])
def handle_add_planet():
    body = request.get_json()
    
    if 'name' not in body:
        return jsonify({'msj': 'name is required'}), 400
    
    if 'diameter' not in body:
        return jsonify({'msj': 'diameter is required'}), 400
    
    if 'rotation_period' not in body:
        return jsonify({'msj': 'rotation_period  is required'}), 400
    
    if 'gravity' not in body:
        return jsonify({'msj': 'gravity is required'}), 400
    
    exist = Planet.query.filter_by(name = body["name"]).first()
    if exist: 
       return jsonify ({"msg":"Planet already exists"})
    
    new_planet = Planet()
    new_planet.name = body['name']
    new_planet.diameter= body['diameter']
    new_planet.rotation_period= body['rotation_period']
    new_planet.gravity= body['gravity']

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def habndle_delete_planet(planet_id):

    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'planet id not exist'}), 404
    db.session.delete(planet)
    db.session.commit()

    return jsonify({"msg": "Deleted planet"}), 204

@app.route('/people', methods=['GET'])
def handle_get_peoples():

    all_peoples = People.query.all()
    if not all_peoples:
        return jsonify({"msg": "Peoples empty"}), 404
    all_peoples = list(map(lambda x: x.serialize(), all_peoples))

    return jsonify(all_peoples), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_get_people(people_id):
    
    people = People.query.get(people_id)
    if not people:
        return jsonify({"msg":"People not exist"}), 404
    people = people.serialize()

    return jsonify(people), 200

@app.route('/people', methods=['POST'])
def handle_add_people():
    body = request.get_json()

    if 'name' not in body:
        return jsonify({'msj': 'name is required'}), 400
    
    if 'hair_color' not in body:
        return jsonify({'msj': 'hair_color is required'}), 400
    
    if 'height' not in body:
        return jsonify({'msj': 'height is required'}), 400
    
    if 'skin_color' not in body:
        return jsonify({'msj': 'skin_color is required'}), 400
    
    if 'gender' not in body:
        return jsonify({'msj': 'gender is required'}), 400
    
    exist = People.query.filter_by(name = body["name"]).first()
    if exist: 
       return jsonify ({"msg":"People already exists"})
    
    new_people = People()    
    new_people.name = body['name']
    new_people.hair_color = body['hair_color']
    new_people.height= body['height']
    new_people.skin_color= body['skin_color']
    new_people.gender= body['gender']

    db.session.add(new_people)
    db.session.commit()

    return jsonify(new_people.serialize()), 201

@app.route('/people/<int:people_id>', methods=['DELETE'])
def habndle_delete_people(people_id):
    people = People.query.get(people_id)
    if not people:
        return jsonify({'msg': 'people id not exist'}), 404
    db.session.delete(people)
    db.session.commit()

    return jsonify({"msg": "Deleted people"}), 204

@app.route('/user/favorites', methods=['GET'])
def handle_get_user_favorites():

    body = request.get_json()    
    user_id = body.get('user_id')
    if not user_id:
        return jsonify({"msg": "user_id are required"}), 400    
    user_exist = User.query.filter_by(id = user_id).first()
    if not user_exist: 
       return jsonify ({"msg":"User not exists"}) 
    
    all_user_fav_planets = Fav_Planet.query.filter_by(user_id=user_id)
    all_user_fav_peoples = Fav_People.query.filter_by(user_id=user_id)

    return jsonify({
        "favorite planets": [planet.serialize() for planet in all_user_fav_planets],
        "favorite people": [people.serialize() for people in all_user_fav_peoples]
    }), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):

    body = request.get_json()
    user_id = body.get('user_id')
    if not user_id:
        return jsonify({"msg": "user_id are required"}), 400
    user_exist = User.query.filter_by(id = user_id).first()
    if not user_exist: 
       return jsonify ({"msg":"User not exists"})                 
    exist = Fav_Planet.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if exist: 
       return jsonify ({"msg":"favorite planet already exists"})
    
    new_fav_planet = Fav_Planet()    
    new_fav_planet.user_id = user_id
    new_fav_planet.planet_id = planet_id

    db.session.add(new_fav_planet)
    db.session.commit()

    return jsonify(new_fav_planet.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):

    body = request.get_json()
    user_id = body.get('user_id')
    if not user_id:
        return jsonify({"msg": "user_id are required"}), 400
    user_exist = User.query.filter_by(id = user_id).first()
    if not user_exist: 
       return jsonify ({"msg":"User not exists"})            
    exist = Fav_People.query.filter_by(user_id = user_id, people_id = people_id).first()
    if exist: 
       return jsonify ({"msg":"Favorite people already exists"})
    
    new_fav_people = Fav_People()    
    new_fav_people.user_id = user_id
    new_fav_people.people_id = people_id

    db.session.add(new_fav_people)
    db.session.commit()

    return jsonify(new_fav_people.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):

    body = request.get_json()
    user_id = body.get('user_id')
    if not user_id:
        return jsonify({"msg": "user_id is required"}), 400    
    user_exist = User.query.filter_by(id = user_id).first()
    if not user_exist: 
       return jsonify ({"msg":"User not exists"})    
    planet_exist = Planet.query.filter_by(id = planet_id).first()
    if not planet_exist: 
       return jsonify ({"msg":"Planet not exists"})     
    fav_planet = Fav_Planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav_planet:
        return jsonify({'msg': 'favorite planet not exist'}), 404
    db.session.delete(fav_planet)
    db.session.commit()

    return jsonify({"msg": "Deleted favorite planet"}), 204

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):

    body = request.get_json()
    user_id = body.get('user_id')
    if not user_id:
        return jsonify({"msg": "user_id are required"}), 400    
    user_exist = User.query.filter_by(id = user_id).first()
    if not user_exist: 
       return jsonify ({"msg":"User not exists"})    
    people_exist = People.query.filter_by(id = people_id).first()
    if not people_exist: 
       return jsonify ({"msg":"People not exists"})    
    fav_people = Fav_People.query.filter_by(user_id=user_id, people_id=people_id).first()
    if fav_people is None:
        return jsonify({'msg': 'favorite people not exist'}), 404
    db.session.delete(fav_people)
    db.session.commit()

    return jsonify({"msg": "Deleted favorite people"}), 204

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
