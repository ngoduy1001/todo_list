from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo

class SignUpForm(FlaskForm):
    full_name = StringField('Full Name')
    email = StringField('Email',
                        validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators = [InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField('Login')