
import datetime
import os
from functools import wraps
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import Flask, Blueprint, request, jsonify, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, auth_token_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from application.models import User, Role, roles_users, Product, Category, Cart, Purchase, Ratings
from flask_httpauth import HTTPTokenAuth
from flask_login import current_user  # Import current_user
from application import db, app, cache
from flask_login import LoginManager, login_user, logout_user, login_remembered
from wtforms.validators import Email
from application.task import check_product_stock
from sqlalchemy import or_
import base64
import uuid

user_bp = Blueprint('user', __name__)

@user_bp.route('/user_profile', methods=['GET','POST'])
@jwt_required()
def user_profile():
    u_id = get_jwt_identity()
    curr_user = User.query.filter_by(id=u_id).first()

    if curr_user:
        user = {
            'username': curr_user.username,
            'email': curr_user.email,
            'phone_number': curr_user.phone_number,
            
        }
        if curr_user.filename:
            from application import UPLOAD_USER_PHOTOS_FOLDER
            photo_path = os.path.join(app.config['UPLOAD_USER_PHOTOS_FOLDER'], curr_user.filename)
            print(photo_path)
            try:
                with open(photo_path, 'rb') as photo_file:
                    # Encode the image file to base64
                    base64_image = base64.b64encode(photo_file.read()).decode('utf-8')
                    user['photo_base64'] = base64_image
            except FileNotFoundError:
                print(f"Photo file not found: {curr_user.filename}")
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404


@user_bp.route('/get_products', methods=['GET'])
@jwt_required()
def get_products():
    user = get_jwt_identity()
    print(user)
    products = Product.query.all()
    product_data = []
    for product in products:
        product_item = {
            'product_id':product.id,
            'item_name': product.name,
            'stock': product.stock,
            'rate_per_unit': product.rate_per_unit,
            'expiry_date' : product.expiry_date,
            'rating': product.rating
        }
        product_data.append(product_item)
    return jsonify(products=product_data), 200
from flask import jsonify, abort

@user_bp.route('/category/<int:category_id>', methods=['GET'])
@cache.cached(timeout=300) 
def get_category(category_id):
    category = Category.query.get(category_id)
    print(category_id)
    if category:
        # Convert category data to a dictionary
        category_data = {
            'id': category.id,
            'name': category.name,
            'products': [
                {
                    'id': product.id,
                    'name': product.name,
                    'stock': product.stock,
                    # Add more product details as needed
                }
                for product in category.products
            ]
        }
        return jsonify(category=category_data)
    else:
       
        return jsonify({'massage':"Category not found"}), 404


@user_bp.route('/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user = get_jwt_identity()
    data = request.get_json()
    item_name = data.get("item_name")
    quantity = data.get("item_quantity")
    curr_product = Product.query.filter_by(name = item_name).first()
    amount = curr_product.rate_per_unit*quantity
    print(quantity)
    print(amount)
    # Check if the item is already in the customer's cart
    existing_item = Cart.query.filter_by(customer_id=user, item_name=item_name).first()
    if existing_item:
        # Update the quantity and total amount if the item already exists in the cart
        existing_item.item_quantity += quantity
        existing_item.total_amount += amount
        db.session.commit()
        curr_product.stock -= quantity
        db.session.commit()
    else:
        # Create a new cart item
        new_item = Cart(customer_id=user, item_name=item_name, item_quantity=quantity, total_amount= amount)
        db.session.add(new_item)
        curr_product.stock -= quantity
        db.session.commit()
    return jsonify({'message': 'Item added to cart successfully'}), 200

@user_bp.route('/view_cart', methods=['GET'])
@jwt_required() 
def view_cart():
    user = get_jwt_identity()
    cart_items = Cart.query.filter_by(customer_id=user).all()
    cart_data = []
    for item in cart_items:
        cart_data.append({
            'item_name': item.item_name,
            'item_quantity': item.item_quantity,
            'total_amount': item.total_amount,
        })
    
    return jsonify(cart_data), 200



@user_bp.route('/purchase_cart', methods=['POST'])
@jwt_required()
def purchase_cart():
    # Check if the cart is empty
    current_user = get_jwt_identity()
    cart_items = Cart.query.filter_by(customer_id=current_user).all()
    if not cart_items:
        return jsonify({'message': 'Your cart is empty'}), 400  # Bad Request

    try:
        # Create a purchase record for each item in the cart
        for item in cart_items:
            product = Product.query.filter_by(name=item.item_name).first()
            print(product)
            purchase = Purchase(
                item_name=item.item_name,
                product_id=product.id,  # Replace with the actual product ID
                item_quantity=item.item_quantity,
                purchase_date=datetime.datetime.utcnow(),  # Adjust as needed
                total_amount=item.total_amount,
                customer_id=current_user,
                feedback='',
            )
            db.session.add(purchase)
        
       
        Cart.query.filter_by(customer_id=current_user).delete()
        db.session.commit()

        return jsonify({'message': 'Items purchased successfully'}), 200  # OK
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred while processing the purchase'}), 500  # Internal Server Error





@user_bp.route("/search", methods=["GET"])
def search_items():
    search_query = request.args.get("q", "").strip()
    
    if not search_query:
        return jsonify({"message": "No search query provided"}), 400

    # List of common English prepositions and articles
    common_words = ["a", "an", "the", "in", "on", "at", "to", "for", "by", "with"]

    keywords = [word.lower() for word in search_query.split() if word.lower() not in common_words]

    # Create a filter condition for each keyword
    product_filters = [Product.name.ilike(f"%{keyword}%") for keyword in keywords]
    category_filters = [Category.name.ilike(f"%{keyword}%") for keyword in keywords]

    product_query = Product.query.filter(or_(*product_filters))
    category_query = Category.query.filter(or_(*category_filters))

    product_results = product_query.all()
    category_results = category_query.all()

    products = [{"name": result.name, "category": result.category.name} for result in product_results]
    categories = [{"name": result.name} for result in category_results]

    return jsonify({"products": products, "categories": categories})



@user_bp.route("/view_product/<int:product_id>", methods=["GET"]) 
def view_product(product_id):
    product = Product.query.filter_by(id = product_id).first_or_404()
    product_data = {
        "name": product.name,
        "stock": product.stock,
        "manufacture_date": product.manufacture_date.strftime("%Y-%m-%d"),
        "expiry_date": product.expiry_date.strftime("%Y-%m-%d"),
        "rate_per_unit": product.rate_per_unit,
        "current_stock": product.current_stock,
        "rating": product.rating,
        "feedback": product.feedback,
        "photo": get_base64_encoded_photo(product.photo_filename),  # Send the base64 encoded photo
    }

    return jsonify(product_data)

def get_base64_encoded_photo(photo_filename):
    try:
        from application import UPLOAD_PRODUCT_PHOTOS_FOLDER
        with open(os.path.join(app.config["UPLOAD_PRODUCT_PHOTOS_FOLDER"], photo_filename), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
    except FileNotFoundError:
        return None

@user_bp.route('/view_category/<int:category_id>')
def view_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()

    # Convert data to JSON format
    category_data = {
        'id': category.id,
        'name': category.name,
    }

    products_data = [{
        'id': product.id,
        'name': product.name,
        'stock': product.stock,
    } for product in products]

    return jsonify({'category': category_data, 'products': products_data})


@user_bp.route("/purchase_product/<int:product_id>", methods=["POST"])
@jwt_required()
def purchase_product(product_id):
    data = request.json
    quantity = data.get('quantity')  

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return jsonify(error="Product not found"), 404

    purchase_date = datetime.utcnow()
    total_amount = product.rate_per_unit * quantity  

    purchase = Purchase(
        item_name=product.name,
        product_id=product.id,
        item_quantity=quantity,
        purchase_date=purchase_date,
        total_amount=total_amount,
        customer_id=get_jwt_identity(),  
        feedback=''
    )

    db.session.add(purchase)
    db.session.commit()

    return jsonify(message=f"Product with ID {product_id} purchased successfully")






