import my_app as app # Tengo que agrergar el as my_app para que lo tome
# from bson import json_util
from bson.objectid import ObjectId
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField,DecimalField
from wtforms.validators import InputRequired,NumberRange

class Product:
    def __init__(self):
        self.nombre = None
        self.marca = None
        self.precio = None

    def get_products(self):
        products = app.db['product'].find()
        # return{
        #     'usuario':self.usuario,
        #     'monto':self.monto,
        #     'tipo':self.tipo,
        # }
        return products
    def get_product(self,id):
        result = app.db['product'].find_one({'_id': ObjectId(id), })
        return result
    
    def create_product(self,product):
        result = app.db['product'].insert_one(product)
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

class ProductForm(FlaskForm):
    nombre = StringField('nombre', validators=[InputRequired()])
    marca = StringField('marca', validators=[InputRequired()])
    precio = DecimalField('precio', validators=[InputRequired(),NumberRange(min=Decimal('0.0'))])