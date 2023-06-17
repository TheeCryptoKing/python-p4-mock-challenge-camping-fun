from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # bidimensional relationship
    signup = db.relationship('Signup', cascade="all,delete",back_populates='activity')
    
    # signups = db.relationship("Signup", cascade="all,delete", backref= "activity")
    
    serialize_only = ("id", "name", "difficulty")

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('name')
    def validate_name(self, key, name):
        # names = db.session.query(Camper.name).all()
        # if not name:
        #     raise ValueError('What you saying Dawg?')
        # return name 
    
        if not name or len(name) < 1: 
            raise ValueError("Name must exist")
        return name
    
    @validates('age')
    def validates_age(self, key, age):
        if not 8 > age > 10:
            raise ValueError("Fuck is you doing dawg?!?!")
        return age
    
        # print('Inside the age validation')
        # if not 8 <= age <= 18: 
        #     print('Invalid!!')
        #     raise ValueError("Age must be 8 to 18")
        # return age
        
    # bidimensional Relationship
    signup = db.relationship('Signup', back_populates='camper')
    # Both can work but would have to alter signups
    # signup = db.relationship("Signup", backref= "camper")

    serialize_rules = ("-signup.camper",)
    
    # needed for  if you require more advanced functionality, such as custom calculations, encapsulation of logic, or a consistent API for accessing related data, 
    activities = association_proxy("signups", "activity")
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'
    
class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    
    # Bidimensional Relationship
    camper_id = db.Column('Camper', ForeignKey('campers.id')) 
    camper = db.relationship('Camper', back_populates='signup')
    activity_id = db.Column('Activity', ForeignKey('activities.id'))
    activity = db.relationship('Activity', back_populates='signup') 
    
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Reason :
    serialize_rules = ("-camper.signup","-activity.signup")
    
    @validates('time')
    def validates_time(self, key, time):
        if time > 23:
            raise ValueError("Make it longer or Shorter HURRY UP!!!")
        return time
    
        # if not 0 <= time <= 23:
        #     raise ValueError("Time must be within limits")
        # return time
    
    def __repr__(self):
        return f'<Signup {self.id}>'


############################ Serialize notes ######################
    # Reason for only: serialize_only attribute is to specify which attributes of the Activity model should be included when serializing an instance of the model into a JSON or another serialized format. By defining serialize_only with a tuple of attribute names, you are instructing the serialization process to include only those attributes in the serialized output.
    # serialize_only attribute, you can control the attributes that are exposed and sent during serialization, ensuring that only the necessary data is included. This can be useful for optimizing network bandwidth, reducing payload size, or controlling the information that is made available to the client.
    
    # Reason: serialize_only: This attribute typically specifies a list or tuple of attribute names that should be included when serializing an object. It allows you to explicitly define which attributes are part of the serialized output, excluding the others. Only the attributes listed in serialize_only will be included in the serialized representation.
    
    # serialize_rules: This attribute could potentially provide more advanced or flexible serialization rules. It might allow you to define custom rules or transformations for each attribute during serialization. For example, you might define rules for attribute renaming, data formatting, or even conditional inclusion/exclusion of certain attributes based on specific conditions or criteria.
    # Attribute renaming, Data formatting, Conditional inclusion/exclusion, Custom transformations
    
    #Cascade behavior determines what actions should be taken on related objects when certain operations occur on the parent object. In this case, the cascade behavior is set to "all,delete". Let's break down what this cascade behavior signifies:

    # all: This cascade option means that all types of cascading operations should be applied. It includes cascading operations such as "save-update", "merge", "refresh", "expunge", and "delete". It ensures that changes made to the parent object, such as saving or deleting it, will be propagated to the related Signup objects.

    # delete: This cascade option specifies that when the parent object (Activity in this case) is deleted, the related Signup objects should also be deleted automatically. In other words, when an Activity is deleted, any associated Signup objects will be deleted as well.

    # By setting the cascade behavior to "all,delete", any changes made to the parent Activity object will be cascaded to the related Signup objects, and deleting an Activity will result in the deletion of associated Signup objects.

# add any models you may need. 