from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,FloatField,PasswordField,EmailField, SubmitField
from wtforms.validators import DataRequired, Length



class SignUpForm(FlaskForm):
    email= EmailField('Email', validators=[DataRequired()])
    name= StringField('Name', validators=[DataRequired()])
    password= PasswordField('Enter Your Password', validators=[DataRequired(), Length(min=6)])
    submit= SubmitField('Sign up')


class LoginForm(FlaskForm):
    email= EmailField('Email', validators=[DataRequired()])
    password= PasswordField('Enter Your Password', validators=[DataRequired(), Length(min=6)])
    submit= SubmitField('Sign in')


class ForgotForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired()])
    password= PasswordField('Enter Your Password', validators=[DataRequired(), Length(min=6)])
    confirmPassword= PasswordField('Enter Your Password', validators=[DataRequired(), Length(min=6)])
    submit= SubmitField('Reset Password')

