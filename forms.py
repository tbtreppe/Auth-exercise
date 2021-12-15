from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators imput InputRequired

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])