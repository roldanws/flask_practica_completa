from flask import Blueprint, render_template, request,redirect,url_for
from my_app.product.model.product import Product
from my_app.product.model.product import ProductForm

from flask_login import login_required
from my_app import rol_admin_need

product = Blueprint('product',__name__)

@product.before_request
@login_required
def constructor():
    pass

@product.route('/')
@product.route('/home')
@rol_admin_need
def products():
    product = Product()
    print("Productos: ",product.get_products())
    products = product.get_products()
    print(type(products))
    return render_template('product/product_list.html', products=products)

@product.route('/product/<id>')
def detail(id):
    product = Product()
    print("Producto: ",product.get_product(id))
    product_result = product.get_product(id)
    return render_template('product/product_detail.html', product=product_result)

@product.route('/create/product', methods=['GET','POST'])
def create():
    form = ProductForm(meta={'csrf':False} )
    if form.validate_on_submit():
        product = {
        'nombre': request.form['nombre'],
        'marca': request.form['marca'],
        'precio': request.form['precio']
        }
        new_product = Product()
        new_product.create_product(product)
        return redirect(url_for('product.products'))
    if form.errors:
        print("Error", form.errors)

    return render_template('product/product_create.html',form=form)


@product.route('/update/product/<id>', methods=['GET','POST'])
def update(id):
    prod = Product() 
    result = prod.get_product(id)
    form = ProductForm(meta={'csrf':False} )

    if request.method == 'GET':
        form.nombre.data=result['nombre']
        form.marca.data=result['marca']
        form.precio.data=float(result['precio'])

    if form.validate_on_submit():

        product = {
        'nombre': request.form['nombre'],
        'marca': request.form['marca'],
        'precio': request.form['precio']
        }
        
        prod.update_product(id,product)
        return redirect(url_for('product.products'))
    if form.errors:
        print("Error", form.errors)
    return render_template('product/product_update.html',id_product=id,form=form)

@product.route('/delete/<id>')
def delete(id):
    product = Product()
    product_result = product.delete_product(id)
    return redirect(url_for('product.products'))
    #return render_template('product/product_list.html', product=product_result)


