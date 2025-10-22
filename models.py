from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hive(db.Model):
    __tablename__ = 'hives'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    honey = db.Column(db.Integer, default=0) 

class Bee(db.Model):
    __tablename__ = 'bees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    pollen = db.Column(db.Integer, default=0)
