from flask import Flask,render_template,request,url_for,redirect,jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from forms import register_form,login_form,todo_form
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///todo.db'
app.config['SECRET_KEY']= 'SECRETKEY'
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

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


@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        return 'validated'
    return render_template('login.html',title = 'Login Page',form= form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = register_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username = form.user_name.data,email = form.email_address.data,password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.user_name.data} !','success')
        return redirect(url_for('login'))
    else:
        print('not validated')
        return render_template('register.html',title = 'Register Page',form = form)

@app.route('/todo',methods = ['GET','POST'])
def todo():
    form= todo_form()
    if form.validate_on_submit():
        data = Todo(text = form.todo.data,complete = False)
        db.session.add(data)
        db.session.commit()
        flash('New Todo added','success')
        return redirect(url_for('todo'))
    else:
        return render_template('todo.html',title= 'output page',incomplete = Todo.query.filter_by(complete = False),\
            complete_data =Todo.query.filter_by(complete = True), form = form)

@app.route('/update_todo',methods = ['POST'])
def update_todo():
    todo_id=request.form.get("todo_id")
    status=request.form.get("todo_status")
    status_bool = False  if status == str(0) else True
    Todo.query.filter_by(id= todo_id ).update(dict(complete = status_bool))
    db.session.commit()
    return redirect(url_for('todo'))
    
@app.route('/delete_all',methods = ['GET'])
def delete_ll():
    rows_deleted = Todo.query.delete()
    db.session.commit()
    return jsonify({'rows_deleted':rows_deleted})

@app.route('/delete<int:post_id>',methods = ['POST'])
def delete():
    if request.method == ["POST"]:
        return f"{request.get('todo_id')}"
    Todo.query.delete()
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True,port = 3000)