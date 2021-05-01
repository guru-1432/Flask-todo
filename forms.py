from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField,SubmitField,BooleanField,IntegerField
# from app import User,Todo
from flask import flash

from wtforms.validators import DataRequired,Length,Email,EqualTo

class register_form(FlaskForm):
    user_name = StringField('Username',validators=[DataRequired('User name is required'),Length (min=2,max=15 )]) # This User name will be used in html
    email_address = StringField('Email',validators=[DataRequired(),Email(message = 'Please provide a valid email address')])
    password = PasswordField('Password',validators=[DataRequired('User name is required')])
    conform_password = PasswordField('Conform_Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign_up')


    
    # def validate_username(self,user_name):
    #     user_db = User.query.filter_by(username = user_name.data).first()
    #     if user_db:
    #         flash(f'User name already exist {user_name.data} !','danger')
            

class login_form(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()]) # This User name will be used in html
    password = PasswordField('Password',validators=[DataRequired()]) # This User name will be used in html
    login = SubmitField('Login') # This User name will be used in html

    
class todo_form(FlaskForm):
    todo = StringField('New Todo',validators=[DataRequired(),Length(min=2,max=30)])
    completed = BooleanField('Completed')
