from flask_wtf import FlaskForm 
from wtforms import IntegerField, StringField, PasswordField, SelectField, BooleanField, SelectMultipleField, DateField, TextAreaField
from wtforms.validators import URL, Optional, InputRequired, DataRequired 

class LoginForm(FlaskForm):
    
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])