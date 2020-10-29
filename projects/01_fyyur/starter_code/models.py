from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)

class Show(db.Model):
	__tablename__ = 'shows'
	id = db.Column(db.Integer, primary_key=True)
	venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
	artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
	start_time = db.Column(db.DateTime, default=datetime.utcnow)
	artists = db.relationship("Artist", backref=db.backref("shows", cascade="all, delete", lazy=True))
	venues = db.relationship("Venue", backref=db.backref("shows", cascade="all, delete", lazy=True))
	

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default= False)
    seeking_description = db.Column(db.String(500))

 	
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default= False)
    seeking_description = db.Column(db.String(500))