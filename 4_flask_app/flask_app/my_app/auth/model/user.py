import my_app as app # Tengo que agrergar el as my_app para que lo tome
# from bson import json_util
from bson.objectid import ObjectId
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField,DecimalField,PasswordField, HiddenField
from wtforms.validators import InputRequired,NumberRange, EqualTo
from werkzeug.security import generate_password_hash,check_password_hash

class User:
    ROL_REGULAR = 1
    ROL_ADMIN = 6
    def __init__(self):
        self.username = None
        self.password = None
        self.rol = User.ROL_REGULAR
        self.id = None

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    def get_user_by_id(self,id):
        print(id)
        result = app.db['user'].find_one({'_id': ObjectId(id)})
        self.username = result['username']
        return result

    
    


    def get_products(self):
        products = app.db['product'].find()
        # return{
        #     'usuario':self.usuario,
        #     'monto':self.monto,
        #     'tipo':self.tipo,
        # }
        return products
    def logout_user(self,username,password):
        pass
    def login_user(self,username,password):
        result = app.db['user'].find_one({'username': username })
        if result:
            password_hash = result['password']
            self.id = str(result['_id'])
            print("Password obtenido:", password)
            print("Id obtenido:", result['_id'], type(str(result['_id'])))
            validation = check_password_hash(password_hash,password)
            self.username = username
            return validation
        else:
            print("No existe el usuario")
            return False

    def get_user(self,username):
        result = app.db['user'].find_one({'username': username })
        return result
    
        
    
    def create_user(self,username, password):
        user = {
        'username': username,
        'password': generate_password_hash(password),
        'rol': self.rol
        }
        result = app.db['user'].insert_one(user)
        return result
    
    def update_product(self,id,product):
        # result = app.db['product'].update_one({
        #     '_id': ObjectId(id)
        # },product)

        #result = app.db['product'].update_one(
        #    {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': product})
        #return result
        
        result = app.db['product'].update_one({'_id': ObjectId(id)}, {'$set':product})
    
    def delete_product(self,id):
        result = app.db['product'].delete_one({'_id': ObjectId(id), })
        return result

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    next = HiddenField('next')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(),EqualTo('confirm')])
    confirm = PasswordField('confirm', validators=[InputRequired()])