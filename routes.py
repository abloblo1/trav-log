from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm, LoginForm
from flask_pymongo import PyMongo
from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)
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
        return redirect(url_for('login'))

    return render_template("home.html")
if __name__ == "__main__":
  app.run(debug=True)
