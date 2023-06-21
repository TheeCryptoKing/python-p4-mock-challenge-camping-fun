#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    return 'Welcome Friend'

# GET /campers
# POST /campers
# GET /campers/int:id
# GET /activities
# POST /signups

class Campers(Resource):
    
    def get(self):
        campers = [c.to_dict(only=('id', 'name', 'age')) for c in Camper.query.all()]
        return campers, 200
        # Working 
    def post(self):
        try:
            data = request.get_json()
            new_camper = Camper(
                name=data.get('name'),
                age=data.get('age')
            )
            db.session.add(new_camper)
            db.session.commit()
            return new_camper.to_dict(), 201
        except:
            raise ({"error": "400: Validation error"}, 400)
        #  Working 
api.add_resource(Campers, '/campers')

class CampersId(Resource):
    def get(self, id):
        camperbyID = Camper.query.filter_by(id=id).first()
        return camperbyID.to_dict(only=('id', 'name', 'age',)), 200
        # working
api.add_resource(CampersId, '/campers/<int:id>')

class Activities(Resource):
    def get(self):
        actitty = [a.to_dict(only=('id', 'name', 'difficulty')) for a in Activity.query.all()]
        return actitty, 200 
    # Working 
api.add_resource(Activities, '/activities')

class ActivitiesId(Resource):
    def get(self, id):
        actitty = Activity.query.filter_by(id=id).first()
        return actitty.to_dict(only=('id', 'name', 'difficulty')), 200 
    # Working
    def delete(self,id):
        try:
        # data = request.get_json()
            actitty = Activity.query.filter_by(id=id).first()
            if actitty:
                Signup.query.filter(actitty.id == id).delete()
                db.session.delete(actitty)
                db.session.commit()
                return make_response({}, 204)
        except:
            return ({"error": "404: Activity not found"}, 404)
        # Working
api.add_resource(ActivitiesId, '/activities/<int:id>')

class Signuper(Resource):
    def get(self):
        try:
            signees = [s.to_dict(only=('time', 'camper_id', 'activity_id')) for s in Signup.query.all()]
            return signees, 200
        except:
            return ({"error": "400: Validation error"}, 400)
        # Working
api.add_resource(Signuper,'/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)