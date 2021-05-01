from flask import render_template,request,url_for,redirect,jsonify,flash
from flask_todo import app,bcrypt,db
from flask_todo.forms import register_form,login_form,todo_form
from flask_todo.models import User,Todo

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