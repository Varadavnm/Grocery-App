import datetime
from functools import wraps
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import Flask, Blueprint, request, jsonify, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, auth_token_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from application.models import User, Role, roles_users, Product, Category, Cart, Purchase
from flask_httpauth import HTTPTokenAuth
from flask_login import current_user  # Import current_user
from application import db, app
from flask_login import LoginManager, login_user, logout_user, login_remembered
from wtforms.validators import Email
from application.task import check_product_stock
import uuid
updates_bp = Blueprint('updates', __name__)
from flask import request, jsonify, Blueprint
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

updates_bp = Blueprint('updates_bp', __name__)

@updates_bp.route('/update_profile', methods=['POST'])
@jwt_required()
def update_profile():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        user = User.query.filter_by(id = user_id).first()
        # Update user information based on the received data
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.address = data.get('address', user.address)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.department = data.get('department', user.department)

        # Check if a new password is provided, and update it if necessary
        new_password = data.get('new_password')
        if new_password:
            user.password = generate_password_hash(new_password, method='sha256')

        # Update the user in the database
        db.session.commit()

        return jsonify({'message': 'User information updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    else:
        return redirect(url_for('login_customer'))
    
@app.route('/get_stock/<product_name>', methods=['GET'])
def get_stock(product_name):
    product = Product.query.filter_by(name=product_name).first()

    if product:
        return jsonify({"stock": product.stock})
    else:
        return jsonify({"error": "Product not found"}), 404
    
    


        
    