from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired
from  wtforms import validators

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),validators.Length(min=4, max=25)])
    email = TextField('Email', [validators.Email("Please enter you email address.")])
    password = PasswordField('Password', validators=[DataRequired(),validators.Length(min=8, max=25)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),validators.Length(min=8, max=25)])
    register = SubmitField('Register')