from flask import Blueprint, render_template, request,session,redirect,url_for
#from werkzeug import abort
from my_app.auth.model.user import User, LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from my_app import login_manager

fauth = Blueprint('fauth',__name__)

@login_manager.user_loader
#def load_user(user_id):
def load_user(id):
    print(id)
    u = User()
    u.get_user_by_id(id)
    u.get_id()
    return u
        

    
@fauth.route('/register', methods=['GET','POST'])
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

@fauth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        print("Ya estas autenticado")
        return redirect(url_for('product.products'))

    form = LoginForm(meta={'csrf':False} )
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        new_user = User()
        result = new_user.login_user(username,password)
        if result: 
            # user = {
            #     'username':username,
            #     'rol':new_user.rol,
            #     'id':new_user.id
            # }
            login_user(new_user)
            print("Login correcto")

            next = request.form['next']
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            #if not is_safe_url(next):
            #    return abort(400)
            return redirect(next or url_for('product.products'))
        else:
            print("Datos incorrectos")
    if form.errors:
        print("Error", form.errors)

    return render_template('auth/login.html',form=form)

@fauth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('fauth.login'))

@fauth.route('/protec')
@login_required
def prote():
    return "Vista protec"