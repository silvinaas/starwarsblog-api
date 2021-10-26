"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    people_query = People.query.all()
# map the results and your list of people  inside of the all_people variable
    all_people = list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_people), 200

@app.route('/people', methods=['POST'])
def add_people():
    people_list = json.loads(request.data)
    print(people_list)
    eye_color = request.json.get("eye_color", "empty")
    #eye_color = "empty"
    #if eye_color != "empty":
    #eye_color = people_list["eye_color"]
    Person = People(name=people_list["name"], gender=people_list["gender"], hair_color=people_list["hair_color"], eye_color=eye_color)
    db.session.add(Person)
    db.session.commit()
    people_query = People.query.all()
# map the results and your list of people  inside of the all_people variable
    all_people = list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['PUT'])
def upd_people(people_id):
    body = json.loads(request.data)
    people = People.query.get(people_id)
    if people is None:
        raise APIException('User not found', status_code=404)
    if "name" in body:
        people.name = body["name"]
    if "gender" in body:
        people.gender = body["gender"]
    db.session.commit()
    people_query = People.query.all()
# map the results and your list of people  inside of the all_people variable
    all_people = list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def del_people(people_id):
    people = People.query.get(people_id)
    if people is None:
        raise APIException('User not found', status_code=404)
    
    db.session.delete(people)
    db.session.commit()
    #get all the people
    people_query = People.query.all()
# map the results and your list of people  inside of the all_people variable
    all_people = list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_people), 200


#Doing the same with planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets_query = Planets.query.all()
# map the results and your list of people  inside of the all_people variable
    all_planets = list(map(lambda x: x.serialize(), planets_query))
    return jsonify(all_planets), 200

@app.route('/planets', methods=['POST'])
def add_planets():
    planets_list = json.loads(request.data)
    print(planets_list)
    eye_color = request.json.get("eye_color", "empty")
    #eye_color = "empty"
    #if eye_color != "empty":
    #eye_color = people_list["eye_color"]
    Planet = Planets(name=planets_list["name"], population=planets_list["population"], terrain=planets_list["terrain"])
    db.session.add(Planet)
    db.session.commit()
    planets_query = Planets.query.all()
# map the results and your list of people  inside of the all_people variable
    all_planets = list(map(lambda x: x.serialize(), planets_query))
    return jsonify(all_planets), 200

@app.route('/planets/<int:planets_id>', methods=['PUT'])
def upd_planets(planets_id):
    body = json.loads(request.data)
    planets = Planet.query.get(planets_id)
    if planets is None:
        raise APIException('User not found', status_code=404)
    if "name" in body:
        planets.name = body["name"]
    if "population" in body:
        planets.population = body["population"]
    db.session.commit()
    planets_query = Planet.query.all()
# map the results and your list of planets  inside of the all_people variable
    all_planets= list(map(lambda x: x.serialize(), planets_query))
    return jsonify(all_planets), 200

@app.route('/planets/<int:planets_id>', methods=['DELETE'])
def del_planets(planets_id):
    planets = Planet.query.get(planets_id)
    if planets is None:
        raise APIException('User not found', status_code=404)
    
    db.session.delete(planets)
    db.session.commit()
    #get all the people
    planets_query = Planet.query.all()
# map the results and your list of people  inside of the all_people variable
    all_planets = list(map(lambda x: x.serialize(), planets_query))
    return jsonify(all_planets), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
