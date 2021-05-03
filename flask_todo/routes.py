from flask import render_template,request,url_for,redirect,jsonify,flash
from flask_todo import app,bcrypt,db
from flask_todo.forms import register_form,login_form,todo_form
from flask_todo.models import User,Todo
from flask_login import login_user, current_user,logout_user

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo'))
    form = login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and (bcrypt.check_password_hash(user.password,form.password.data)):
            login_user(user,remember = True)
            return redirect(url_for('todo'))
        else:
            flash("Incorrect User Name or Passowrd please retry",'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html',title = 'Login Page',form= form)


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('todo'))
    form = register_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username = form.user_name.data,email = form.email_address.data,password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.user_name.data} !','success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html',title = 'Register Page',form = form)

@app.route('/todo',methods = ['GET','POST'])
def todo():
    form= todo_form()
    if form.validate_on_submit():
        print('todo validated')
        data = Todo(text = form.todo.data,complete = False,current_user = current_user)
        db.session.add(data)
        db.session.commit()
        flash('New Todo added','success')
        return redirect(url_for('todo'))
    else:
        return render_template('todo.html',title= 'output page',incomplete = Todo.query.filter_by(user_id = current_user.id,complete = False),\
            complete_data =Todo.query.filter_by(user_id = current_user.id,complete = True), form = form)

@app.route('/update_todo',methods = ['POST'])
def update_todo():
    todo_id=request.form.get("todo_id")
    status=request.form.get("todo_status")
    status_bool = False  if status == str(0) else True
    Todo.query.filter_by(id= todo_id ).update(dict(complete = status_bool))
    db.session.commit()
    return redirect(url_for('todo'))
    
@app.route('/delete_all',methods = ['GET'])
def delete_all():
    rows_deleted = Todo.query.delete()
    db.session.commit()
    return jsonify({'rows_deleted':rows_deleted})

@app.route('/logout',methods = ['GET'])
def logout():
    print((current_user.id))
    logout_user()
    return redirect(url_for('login'))