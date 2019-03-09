from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, Regexp

class SignupForm(Form):
    first_name = StringField('First name', [DataRequired('Please enter your first name.')])
    last_name = StringField('Last name', [DataRequired('Please enter your last name')])
    email = StringField('Email', [DataRequired('Please enter an email'), Email("Please enter a valid email")])
    password = PasswordField('Password', [DataRequired('Please enter a password'), Length(min=6, message="Password must be 6 characters or more")])
    submit = SubmitField('Sign up', [DataRequired()])

class LoginForm(Form):
    email = StringField('Email', [DataRequired('Please enter your email address.'), Email('Please enter a valid email')])
    password = PasswordField('Password', [DataRequired('Please enter a password.')])
    submit = SubmitField('Sign in')

class FlightsForm(Form):
    origin = StringField('Home city', [DataRequired('Please enter your home city')])
    destination = StringField('Destination city')
    departure_date = StringField('Date')
    submit = SubmitField('Search for flights')
class JournalForm(Form):
    journal_entry = StringField('Journal Entry')
    journal_image = FileField('Upload Image', [Regexp(u'^[^/\\\\]\.jpg$')])
    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
    submit = SubmitField('Submit journal entry')
