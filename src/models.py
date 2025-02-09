from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(32), unique=False, nullable=True) 
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name":self.name,
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.Integer, unique=False, nullable=False)
    img = db.Column(db.String(250), unique=False, nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter":self.diameter,
            "rotation_period":self.rotation_period,
            "gravity": self.gravity,
            "img": self.img,
        }
    
class People(db.Model):
    __tablename__ = 'People'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    hair_color = db.Column(db.String(20), unique=True, nullable=False)
    height = db.Column(db.String(20), unique=True, nullable=False)
    skin_color = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(20), unique=True, nullable=False)
    img = db.Column(db.String(250), unique=False, nullable=True)

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
            "img": self.img,
        }
