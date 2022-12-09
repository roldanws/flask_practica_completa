from flask import Blueprint, render_template, request,session,redirect,url_for
from my_app.auth.model.user import User, LoginForm, RegisterForm

auth = Blueprint('auth',__name__)

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(meta={'csrf':False} )
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        new_user = User()
        result = new_user.get_user(username)
        if result: 
            print("Ya existe el usuario")
        else:
            new_user.create_user(username, password)
            return redirect(url_for('auth.register'))
    if form.errors:
        print("Error", form.errors)
    return render_template('auth/register.html',form=form)

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(meta={'csrf':False} )
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        new_user = User()
        result = new_user.login_user(username,password)
        if result: 
            session['username'] = username
            session['rol'] = new_user.rol
            session['id'] = new_user.id
            print("Login correcto")
            return redirect(url_for('product.products'))
        else:
            print("Datos incorrectos")
    if form.errors:
        print("Error", form.errors)

    return render_template('auth/login.html',form=form)

@auth.route('/logout')
def logout():
    session.pop('username')
    session.pop('rol')
    session.pop('id')
    return redirect(url_for('auth.login'))
