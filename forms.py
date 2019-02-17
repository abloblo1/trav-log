from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
    first_name = StringField('First name', [DataRequired('Please enter your first name.')])
    last_name = StringField('Last name', [DataRequired('Please enter your last name')])
    email = StringField('Email', [DataRequired('Please enter an email'), Email("Please enter a valid email")])
    password = PasswordField('Password', [DataRequired('Please enter a password'), Length(min=6, message="Password must be 6 characters or more")])
    submit = SubmitField('Sign up', [DataRequired()])

class LoginForm(Form):
    email = StringField('Email', [DataRequired('Please enter your email address.'), Email('Please enter a valid email')])
    password = PasswordField('Password', [DataRequired('Please enter a password.')])
    submit =SubmitField('Sign in')
