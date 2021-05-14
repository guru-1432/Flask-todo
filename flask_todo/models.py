from flask_todo import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False) 
    email= db.Column(db.String(120),unique=True, nullable=False) 
    password= db.Column(db.String(60), nullable=False) 
    todo = db.relationship('Todo',backref = 'current_user')

    def __repr__(self):
        return f'User_name: {self.username} Email: {self.email}'
    
    # def get_id(self):
    #     return f'{self.username}'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200)) 
    complete = db.Column(db.Boolean) 
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'todo_id :{self.id} user_id :{self.user_id}'

db.create_all()