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

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

amadeus = Client(
    client_id='rE3dpAsJ6OAlUpa2Huh7t6QrJj2wvNSG',
    client_secret='JGonMzgZuO4J1yJU'
)

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'trav_log'
app.config['MONGO_URI'] = 'mongodb://user:travlog1234@ds145895.mlab.com:45895/trav_log'

mongo = PyMongo(app)

app.secret_key = "development-key"
loggedIn = False

@app.route("/")
def index():
  return render_template("index.html", loggedIn=False)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=['GET','POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        client = mongo.db.users
        if client.find_one({'email': request.form['email']}) is not None:
            flash('An account with that user already exists')
            return redirect(url_for('login'))
            # return redirect(url_for('login'))
        else:
            user = client.insert({'firstname': request.form['firstname'],
                                'lastname': request.form['lastname'],
                                'email': request.form['email'],
                                'password': generate_password_hash(request.form['password']),
                                'journals':[],
                                'flights':[],
                                })
            session['email'] = request.form['email']
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('signup.html')
    else:
        return render_template('signup.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        client = mongo.db.users
        email = request.form['email']
        password = request.form['password']
        user = client.find_one({'email': email})
        if user is not None and check_password_hash(user['password'], password):
            session['email'] = request.form['email']
            loggedIn = True
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('email', None)
    return render_template("index.html", loggedIn=False)

@app.route("/home", methods=['GET','POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('home'))
    return render_template("index.html", loggedIn=True)

@app.route("/flights", methods=['GET','POST'])
def flights():
    if 'email' not in session:
        return redirect(url_for('login'))

    with open('new_city_codes.json') as city_codes:
        data = json.load(city_codes)

    # form = FlightsForm()
    # if form.validate_on_submit():
        # get data from form
    if request.method == 'POST':
        output = ""
        origin = 'Madrid'
        destination = request.form['destination']
        departure_date = request.form['departure']
        flight_info = amadeus.shopping.flight_offers.get(origin=data[origin], destination=data[destination], departureDate=departure_date)
        for i in range(len(flight_info.data[0]['offerItems'][0]['services'][0]['segments'])):
            print(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['departure'])
            print(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['arrival'])
            print(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['carrierCode'])
            print(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['number'])
            output += 'Departure\nAirport: {0}\nDate: {1}\n'.format(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['departure']['iataCode'], flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['departure']['at'])
            output += 'Arrival\nAirport: {0}\nDate: {1}\n'.format(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['arrival']['iataCode'], flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['arrival']['at'])
            output += 'Carrier: {0}'.format(flight_info.data[0]['offerItems'][0]['services'][0]['segments'][i]['flightSegment']['carrierCode'])
            print(output)
        return render_template('flights.html', loggedIn=True)
    elif request.method == 'GET':
        return render_template('flights.html', loggedIn=True)
    else:
        return render_template('flights.html', loggedIn=True)

@app.route("/hotels", methods=['GET','POST'])
def hotels():
    if 'email' not in session:
        return redirect(url_for('login'))
    with open('new_city_codes.json') as city_codes:
        data = json.load(city_codes)
    if request.method == 'POST':
        city = request.form['cities']
        hotel_info = amadeus.shopping.hotel_offers.get(cityCode = data[city])
        output = ""
        for i in range(len(hotel_info.data)):
            output += 'Hotel: {0}\n'.format(hotel_info.data[i]['hotel']['name'])
            output += 'Address: {0} {1} {2}\n'.format(hotel_info.data[i]['hotel']['address']['lines'][0], hotel_info.data[i]['hotel']['address']['postalCode'], hotel_info.data[i]['hotel']['address']['cityName'], hotel_info.data[i]['hotel']['address']['countryCode'])
            output += 'Contact: {0}\n'.format(hotel_info.data[i]['hotel']['contact']['phone'])
            output += 'Amenities: '
            for j in range(len(hotel_info.data[i]['hotel']['amenities'])):
                output += '{0} '.format(hotel_info.data[i]['hotel']['amenities'][j])
            output += '\Available: {0}\n'.format(hotel_info.data[i]['available'])
            output += 'Offers: \nID: {0}\nDescription: {1}\nPrice: {2}{3}\n'.format(hotel_info.data[i]['offers'][0]['id'], hotel_info.data[i]['offers'][0]['room']['description']['text'], hotel_info.data[i]['offers'][0]['price']['total'], hotel_info.data[i]['offers'][0]['price']['currency'])
        print(output)
        return render_template('hotels.html', loggedIn=True)
    elif request.method == 'GET':
        return render_template('hotels.html', loggedIn=True)
    else:
        return render_template('hotels.html', loggedIn=True)

@app.route("/tourism", methods=['GET','POST'])
def tourism():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("tourism.html")

@app.route("/journal_entry", methods=['GET','POST'])
def journal():
    if 'email' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        if 'journal_image' in request.files:
            #get data from journal forms
            journal_image = request.files['journal_image']

            client = mongo.db.users
            journal_image_name = secure_filename(journal_image.filename)
            if allowed_file(journal_image_name):
                journal_image_name = uuid.uuid4().hex
                mongo.save_file(journal_image_name, journal_image)
                journal_entry = {
                    'date': request.form['date'],
                    'entry': request.form['entry'],
                    'image': journal_image_name
                }
                client.update_one({'email':session['email']}, {'$push': {'journals': journal_entry}})
            else:
                flash('Incorrect file type')
            return render_template('journal.html')
    elif request.method == 'GET':
        return render_template('journal.html')
    else:
        return render_template('journal.html')

@app.route("/file/<filename>")
def file(filename):
	return mongo.send_file(filename)

@app.route("/journal", methods=['GET', 'POST'])
def image():
    user = mongo.db.users.find_one({'email': session['email']})
    journal = user['journals']
    if request.method == "POST":
        for i in range(len(journal)):
            if journal[i]['date'] == request.form['date']:
                journal = journal[i]
                break
        return render_template('journal.html', firstname=user['firstname'], entry=journal['entry'], filename=url_for('file', filename=journal['image']))
    elif request.method == 'GET':
        return render_template('journal.html', firstname=user['firstname'])
    else:
        return render_template('journal.html', firstname=user['firstname'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## fix the home page
if __name__ == "__main__":
  app.run(debug=True)
