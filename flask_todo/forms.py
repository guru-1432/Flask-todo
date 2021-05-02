from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_todo.models import User,Todo

class register_form(FlaskForm):
    user_name = StringField('Username',validators=[DataRequired('User name is required'),Length (min=2,max=15 )]) # This User name will be used in html
    email_address = StringField('Email',validators=[DataRequired(),Email(message = 'Please provide a valid email address')])
    password = PasswordField('Password',validators=[DataRequired('User name is required')])
    conform_password = PasswordField('Conform_Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign_up')
    
    def validate_user_name(self,user_name):
        user_db = User.query.filter_by(username = user_name.data).first()
        if user_db:
           raise ValidationError ('This user name is already taken please use a different one')
            
    def validate_email_address(self,email_address):
        email_db = User.query.filter_by(email= email_address.data).first()
        if email_db:
           raise ValidationError ('This email is already taken please use a different one')

class login_form(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email('Please enter a valid email address')]) # This User name will be used in html
    password = PasswordField('Password',validators=[DataRequired()])
    login = SubmitField('Login') 
    
    
class todo_form(FlaskForm):
    todo = StringField('New Todo',validators=[DataRequired(),Length(min=2,max=30)])
    completed = BooleanField('Completed')
