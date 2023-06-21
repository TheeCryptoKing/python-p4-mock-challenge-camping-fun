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

    signups = db.relationship('Signup', back_populates='activity')
    campers = association_proxy('signups', 'camper')
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Add serialization rules
    serialize_only = ("-created_at","-updated_at","-signups.activity",)
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    signups = db.relationship('Signup', back_populates='camper')
    activities = association_proxy('signups', 'activity')
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    serialize_only = ("-created_at","-updated_at","-signups.camper",)
    
    # Add validation
    @validates('name')
    def validates_name(self, key, name):
        if not name or len(name) < 1:
            raise TypeError('Fix Camper name')
        return name 
    
    @validates('age')
    def validates_age(self, key, age):
        if 8 > age > 18:
            raise ValueError('Fix age amount')
        return age
    
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    camper_id = db.Column(db.Integer, ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, ForeignKey('activities.id'))
    
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # serialize_only = ("-created_at","-updated_at","-camper.signups",)
    # "-activity.signups"
    # Add validation
    @validates('time')
    def validates_time(self, key, time):
        if time > 23:
            raise ValueError('Fix the Signup Time')
        return time 
    


# add any models you may need.



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