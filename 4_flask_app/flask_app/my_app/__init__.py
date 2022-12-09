from flask import Flask, url_for, redirect
from pymongo import MongoClient
from flask_login import LoginManager, current_user, logout_user
from functools import wraps

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "fauth.login"

def rol_admin_need(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print(current_user.rol)
        if current_user.rol != 1:
            logout_user()
            print("Debes ser admin para acceder a esta vista")
            return redirect(url_for('fauth.login'))

        return f(*args, **kwds)
    return wrapper

from my_app.product.views import product
from my_app.auth.views import auth
from my_app.fauth.views import fauth
import certifi
#importar vistas
app.register_blueprint(product)
#app.register_blueprint(auth)
app.register_blueprint(fauth)




app.config['DATABASE_URI'] =  "mongodb+srv://admin:admin1234@cluster0.dalbuox.mongodb.net/?retryWrites=true&w=majority"
DATABASE_URI = "mongodb+srv://admin:admin1234@cluster0.dalbuox.mongodb.net/?retryWrites=true&w=majority"

ca = certifi.where()
cliente = MongoClient(DATABASE_URI, tlsCAFile=ca)

db =  cliente['prueba'] 

#except ConnectionError:
#print("Error en la conexion con la db")

