from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=True) 
    password = db.Column(db.String(80), nullable=False)

    fav_planets = db.relationship("Fav_Planet", back_populates="user",cascade="all, delete-orphan")
    fav_peoples = db.relationship("Fav_People", back_populates="user",cascade="all, delete-orphan")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name":self.name,
            "fav_planets": [fav.planet.serialize() for fav in self.fav_planets],
            "fav_peoples": [fav.people.serialize() for fav in self.fav_peoples]
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(250))

    fav_planets = db.relationship("Fav_Planet", back_populates="planet",cascade="all, delete-orphan")

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter":self.diameter,
            "rotation_period":self.rotation_period,
            "gravity": self.gravity,
            "img": self.img
        }
    
class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    hair_color = db.Column(db.String(20), unique=True, nullable=False)
    height = db.Column(db.String(20), unique=True, nullable=False)
    skin_color = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(20), unique=True, nullable=False)
    img = db.Column(db.String(250))

    fav_peoples = db.relationship("Fav_People", back_populates="people",cascade="all, delete-orphan")

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color":self.hair_color,
            "height":self.height,
            "skin_color": self.skin_color,
            "gender": self.gender,
            "img": self.img
        }
    
class Fav_Planet(db.Model):
    __tablename__ = 'fav_planet'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', back_populates="fav_planets")
    planet = db.relationship('Planet', back_populates="fav_planets")

    def __repr__(self):
        return '<Favorites_Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet":self.planet.serialize()
        }  
    
class Fav_People(db.Model):
    __tablename__ = 'fav_people'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', back_populates="fav_peoples")
    people = db.relationship('People', back_populates="fav_peoples")

    def __repr__(self):
        return '<Favorites_people %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "people":self.people.serialize()
        }  