from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask import Blueprint
from sqlalchemy import Column, Integer, String, Float
from werkzeug.security import generate_password_hash, check_password_hash
from application import db
import uuid


roles_users = db.Table('role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False) 
    phone_number = db.Column(db.String(20), nullable=False)  
    department = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)  # Set a default value
    filename = db.Column(db.String(255), nullable=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    last_login_time = db.Column(db.String(255), nullable=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    purchases = db.relationship('Purchase', back_populates='customer')
    ratings = db.relationship('Ratings', back_populates = 'users' )


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(50),nullable=False)  
    description = db.Column(db.String(255))
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', back_populates='category')
    def __init__(self, name):
        self.name = name

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    manufacture_date = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    rate_per_unit = db.Column(db.Float, nullable=False)
    current_stock = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float)
    feedback = db.Column(db.String, nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    # Define the relationship with Category
    category = db.relationship('Category', back_populates='products')
    ratings = db.relationship('Ratings', back_populates = 'product' )
    def __init__(self, name, stock, manufacture_date, expiry_date, rate_per_unit, current_stock, rating, feedback, photo_filename=None):
        self.name = name
        self.stock = stock
        self.manufacture_date = manufacture_date
        self.expiry_date = expiry_date
        self.rate_per_unit = rate_per_unit
        self.current_stock = current_stock
        self.rating = rating
        self.feedback = feedback
        self.photo_filename = photo_filename

class Ratings(db.Model):
    __tablename__ = 'Ratings'
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    review = db.Column(db.String(100), nullable=True)
    revie_number =  db.Column(db.Integer, nullable = True)
    product = db.relationship('Product', back_populates='ratings')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('User', back_populates='ratings')
    
class Purchase(db.Model):
    __tablename__ = 'purchase'
    order_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    item_quantity = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('User', back_populates='purchases')
    def __init__(self, item_name, product_id, item_quantity, purchase_date, total_amount, customer_id, feedback):
        self.item_name = item_name
        self.product_id = product_id
        self.item_quantity = item_quantity
        self.purchase_date = purchase_date
        self.total_amount = total_amount
        self.customer_id = customer_id
        self.feedback = feedback

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_name = db.Column(db.String(100), nullable=False)
    item_quantity = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    def __init__(self, customer_id, item_name, item_quantity, total_amount):
        self.customer_id = customer_id
        self.item_name = item_name
        self.item_quantity = item_quantity
        self.total_amount = total_amount
# Categories:
#     Men:
#     women:
#     kid(boys, girls, teens):
    

# Product:
#     name :
#     Category :
    # type of product
    # Description:
    # colour:
    # price
    # discount:
    # seller:
    # manufacture_date:
    
#     material:



    

    
    
        


    
    