import json
import os
import uuid
import io
from PIL import Image
from bson import Binary
from flask import Flask, render_template, request, session, redirect, url_for, flash
from forms import SignupForm, LoginForm, FlightsForm, JournalForm
from flask_pymongo import PyMongo
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from amadeus import Client, ResponseError, Location

UPLOAD_FOLDER = '/user_images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

amadeus = Client(
    client_id='rE3dpAsJ6OAlUpa2Huh7t6QrJj2wvNSG',
    client_secret='JGonMzgZuO4J1yJU'
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_DBNAME'] = 'trav_log'
app.config['MONGO_URI'] = 'mongodb://user:travlog1234@ds145895.mlab.com:45895/trav_log'

mongo = PyMongo(app)

app.secret_key = "development-key"

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=['GET','POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        client = mongo.db.users
        if client.find_one({'email': form.email.data}) is not None:
            flash('An account with that user already exists')
            return redirect(url_for('signup'))
            # return redirect(url_for('login'))
        else:
            user = client.insert({'firstname': form.first_name.data,
                                'lastname': form.last_name.data,
                                'email': form.email.data,
                                'password': generate_password_hash(form.password.data)})

            session['email'] = form.email.data
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)
    else:
        return render_template('signup.html', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        client = mongo.db.users
        email = form.email.data
        password = form.password.data
        user = client.find_one({'email': email})
        if user is not None and check_password_hash(user['password'], password):
            session['email'] = form.email.data
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route("/home", methods=['GET','POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('home'))

    return render_template("index.html")

@app.route("/flights", methods=['GET','POST'])
def flights():
    if 'email' not in session:
        return redirect(url_for('login'))

    with open('new_city_codes.json') as city_codes:
        data = json.load(city_codes)

    form = FlightsForm()
    if form.validate_on_submit():
        origin = form.origin.data
        destination = form.destination.data
        departure_date = form.departure_date.data
        output = ""
        flight_info = amadeus.shopping.flight_offers.get(origin=data[origin], destination=data[destination], departureDate=departure_date)
        for i in range(len(flight_info.data[0]['offerItems'][0]['services'][0]['segments'])):
            print(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['departure'])
            print(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['arrival'])
            print(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['carrierCode'])
            print(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['number'])
            output += 'Departure\nAirport: %s\nDate: %s\n' % (flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['departure']['iataCode'], flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['departure']['at'])
            output += 'Arrival\nAirport: %s\nDate: %s\n\n' % (flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['arrival']['iataCode'], flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['arrival']['at'])
            output += 'Carrier: %s' % (flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['carrierCode'])
        return render_template('flights.html', form=form, output=output)
    elif request.method == 'GET':
        return render_template('flights.html', form=form)
    else:
        return render_template('flights.html', form=form)

@app.route("/hotels", methods=['GET','POST'])
def hotels():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("hotels.html")

@app.route("/tourism", methods=['GET','POST'])
def tourism():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("tourism.html")

@app.route("/journal", methods=['GET','POST'])
def journal():
    if 'email' not in session:
        return redirect(url_for('login'))
    if 'journal_image' in request.files:
        journal_image = request.files['journal_image']
        client = mongo.db.users
        journal_image_name = secure_filename(journal_image.filename)
        if allowed_file(journal_image_name):
            journal_image_name = uuid.uuid4().hex
            mongo.save_file(journal_image_name, journal_image)
            client.update_one({'email':session['email']}, {"$set": {'image': journal_image_name}}, upsert=False)
        flash('Incorrect file type')
        return render_template('journal.html')
    elif request.method == 'GET':
        return render_template('journal.html')
    else:
        return render_template('journal.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## fix the home page
if __name__ == "__main__":
  app.run(debug=True)
