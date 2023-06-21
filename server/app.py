#!/usr/bin/env python3
# use flask for thunder client or postman 
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

# Had no Home route 
@app.route('/')
def home():
    return ''

class Campers(Resource):
    
    def get(self):
        try:
            # data = request.get_json()
            data = Camper.query.all()
            campers = [camper.to_dict() for camper in data]
            
            return make_response(jsonify(campers), 200)
        
        except:
            return { "error" : "400 Validation error" }, 400
        
    def post(self):
        try:
            # data = request.get_json()
            # request.json can also be used 
            # new_camper = Camper(
                # name = data['name'], age = data['age']
                # )
            # db.session.add(new_camper)
            # db.session.commit()
            new_camper = Camper(
                name= request.json['name'],
                age = request.json['age']
            )
            db.session.add(new_camper)
            db.session.commit()
            return new_camper.to_dict(), 201
            # either to_dict( or jsonify for JSON)
        except:
            return { "error": "400: Validation error" }, 400
        
api.add_resource(Campers, '/campers')

class CampersID(Resource):
    # need a serialize_rules for this table
    def get(self, id):
        try:
            campersbyid = Camper.query.filter_by(id=id).first().to_dict()
            # campersbyid = Camper.query.filter(Camper.id=id).first()
            return make_response(jsonify(campersbyid), 200)
        except:
            return { "error" : "404: Camper not found" }, 404
        
api.add_resource(CampersID, '/campers/<int:id>')
# Working 
class Activities(Resource):
    # GET
        def get(self):
            try:
                activities = Activity.query.all()
                actitites = [activity.to_dict() for activity in activities]
                return make_response(actitites, 200)
        
            except: 
                return {"error":"400 validation error"}, 400
            
api.add_resource(Activities, '/activities')

class ActivitiesID(Resource):
#     # DELETE
#     # i dont understand why a patch is needed
#     def patch(self, id):
#         try:
#             data = request.get_json()
#             #  request.json()
#             activity = Activity.query.filter_by(id = id).first()
#             if request.json['name']:
#                 setattr(activity, 'name', data['name'])
#             db.session.add(activity)
#             db.session.commit()
#             return activity.to_dict(), 202
#         except:
#             raise Exception("error")

    def delete(self, id):
        try:
            # del_signup = Signup.query.filter_by(id=id).first()
            del_activity = Activity.query.filter_by(id=id).first()
            # db.session.delete(del_signup)
            db.session.delete(del_activity)
            db.session.commit()
            # return just has to be a object
            return {}, 204
        except:
            return {"error": "404: Activity not found"}, 404
        
api.add_resource(ActivitiesID, '/activities/<int:id>')

class Signups(Resource):
    # POST
    def post(self):
        try:
            data = request.get_json()
            new_Signup = Signup(
                time=data.get('time'),
                camper_id=data.get('camper_id'),
                activity_id=data.get('activity_id')
            )
            db.session.add(new_Signup)
            db.session.commit()
            return new_Signup.to_dict(), 201
        except:
            return {"error": "400: Validation error"}, 400
api.add_resource(Signups, '/signups')

# data = request.get_json()
# use a .get after when grabbing data
# implememtn try and except

if __name__ == '__main__':
    app.run(port=5555, debug=True)
