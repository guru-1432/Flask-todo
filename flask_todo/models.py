from flask_todo import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False) 
    email= db.Column(db.String(120),unique=True, nullable=False) 
    password= db.Column(db.String(60), nullable=False) 
    todo = db.relationship('Todo',backref = 'current_user')

    def __repr__(self):
        return f'User_name: {self.username} Email: {email}'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200)) 
    complete = db.Column(db.Boolean) 
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f'todo_id :{self.id} user_id :{user_id}'
