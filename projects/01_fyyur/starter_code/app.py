#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# DONE: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
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
    # artists = db.relationship("Artist", secondary="shows")
#    artists = db.relationship('Artist', secondary=Show, backref=db.backref('venues', lazy=True))
    # DONE: implement any missing fields, as a database migration using Flask-Migrate
 	
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
    # venues = db.relationship("Venue", secondary="shows")
    #venues = db.relationship('Venue', secondary=Show, backref=db.backref('artists', lazy=True))
 

    # DONE: implement any missing fields, as a database migration using Flask-Migrate

# DONE: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='full'):
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  areas = Venue.query.distinct(Venue.state, Venue.city).all()
  data= Venue.query.all()
  # num_upcoming_shows per Venue
  upcoming_shows = db.session.query(Show.venue_id, func.count(Show.venue_id)).group_by(Show.venue_id).filter(Show.start_time > datetime.now()).all()
 
  return render_template('pages/venues.html', areas=areas, venues=data, upcoming_shows=upcoming_shows)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE replace with real venue data from the venues table, using venue_id
  upcoming_shows = db.session.query(Show, Artist).join(Show, Show.artist_id == Artist.id).filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).distinct()
  past_shows = db.session.query(Show, Artist).join(Show, Show.artist_id == Artist.id).filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).distinct()

  data = Venue.query.get(venue_id)
  return render_template('pages/show_venue.html', venue=data, upcoming_shows = upcoming_shows, past_shows = past_shows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
	# DONE: insert form data as a new Venue record in the db, instead
	# DONE: modify data to be the data object returned from db insertion
	error = False
	body = {}
	try:
		name = request.form.get('name')
		state = request.form.get('state')
		city = request.form.get('city')
		address = request.form.get('address')
		phone = request.form.get('phone')
		genres = request.form.get('genres')
		facebook = request.form.get('facebook')
		image_link = request.form.get('image_link')
		website = request.form.get('website')
		seeking_talent = request.form.get('seeking_talent')
		seeking_description = request.form.get('seeking_description')
		venue = Venue(name=name, state=state, city=city, address=address, phone=phone, genres=genres, facebook_link=facebook, image_link=image_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
		db.session.add(venue)
		db.session.commit()
	# on successful db insert, flash success
		flash('Venue ' + request.form['name'] + ' was successfully listed!')
	except:
		db.session.rollback()
		error = True
		print(sys.exc_info())
	finally:
		db.session.close()
	if error:
		flash('Venue ' + request.form['name'] + ' could not be listed!')
		flash(sys.exc_info())
		abort(500)


	return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # DONE: BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    error = False
    print("VENUE ID: ", venue_id)
    try:
        venue = Venue.query.get(venue_id)
        shows = db.session.query(Show).filter(Show.venue_id==venue_id)
        print ("SHOWS: ", shows)
        
        # Delete associated shows first before deleting the venue
        for show in shows:
        	db.session.delete(show)

        db.session.delete(venue)
        
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
    	return jsonify({'success': True})

    #Redirect to the home page	
    # render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
	# DONE: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real venue data from the venues table, using venue_id

  upcoming_shows = db.session.query(Show, Venue).join(Show, Show.venue_id == Venue.id).filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).distinct()
  past_shows = db.session.query(Show, Venue).join(Show, Show.venue_id == Venue.id).filter(Show.artist_id == artist_id, Show.start_time < datetime.now()).distinct()

  data = Artist.query.get(artist_id)
  return render_template('pages/show_artist.html', artist=data, upcoming_shows=upcoming_shows, past_shows=past_shows)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
  # 	: modify data to be the data object returned from db insertion

	error = False
	body = {}
	try:
		name = request.form.get('name')
		state = request.form.get('state')
		city = request.form.get('city')
		address = request.form.get('address')
		phone = request.form.get('phone')
		genres = request.form.get('genres')
		facebook = request.form.get('facebook')
		image_link = request.form.get('image_link')
		website = request.form.get('website')
		seeking_talent = request.form.get('seeking_talent')
		seeking_description = request.form.get('seek_description')
		artist = Artist(name=name, state=state, city=city, address=address, phone=phone, genres=genres, facebook_link=facebook, image_link=image_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
		db.session.add(artist)
		db.session.commit()
# on successful db insert, flash success
		flash('Artist ' + request.form['name'] + ' was successfully listed!')
		
	except():
		db.session.rollback()
		error = True
		print(sys.exc_info())
	finally:
		db.session.close()
	if error:
		flash('Artist ' + request.form['name'] + ' could not be listed!')
		flash(sys.exc_info())
		abort(500)


	return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data = db.session.query(Venue, Artist, Show).join(Show, Show.artist_id == Artist.id or Show.venue_id == Venue.id).distinct(Show.id).all()
  data = db.session.query(Venue, Artist, Show).filter(Show.artist_id == Artist.id, Show.venue_id == Venue.id).distinct(Show.id).all()
  print (data)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
	error = False
	body = {}
	try:
		artist_id = request.form.get('artist_id')
		venue_id = request.form.get('venue_id')
		start_time = request.form.get('start_time')
		show_data = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
		db.session.add(show_data)
		db.session.commit()
# on successful db insert, flash success
		flash('A new show is successfully listed!')
	except():
		db.session.rollback()
		error = True
		print(sys.exc_info())
	finally:
		db.session.close()
	if error:
		flash('ERROR: The show could not be listed!')
		flash(sys.exc_info())
		abort(500)

	return render_template('pages/home.html')

  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
