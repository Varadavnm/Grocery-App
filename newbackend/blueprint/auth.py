import base64
import datetime
from functools import wraps
import json
import os
from jwt import ExpiredSignatureError, InvalidTokenError
# from flask.json import JSONEncoder
from flask import Flask, Blueprint, request, jsonify, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, auth_required, login_required, roles_required, auth_token_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from application.models import User, Role, roles_users, Product, Category, Cart, Purchase
from flask_httpauth import HTTPTokenAuth
from werkzeug.utils import secure_filename
from flask_login import current_user  # Import current_user
from application import ALLOWED_EXTENSIONS, db, app, cache
from flask_login import LoginManager, login_user, logout_user
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies, create_access_token, JWTManager
from wtforms.validators import Email
import uuid
from application.permissions import Temp_Manager
from application.report import generate_daily_purchase_bar_chart

login_manager = LoginManager()
login_manager.init_app(app)
auth_bp = Blueprint('auth', __name__)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
jwt = JWTManager(app)


@login_manager.user_loader
def load_user(user_id):
    # Replace this with your actual user loading logic
    return User.query.get(int(user_id))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_role():
    # Check if the roles already exist
    admin_role = Role.query.filter_by(name='admin').first()
    customer_role = Role.query.filter_by(name='customer').first()
    manager_role = Role.query.filter_by(name='manager').first()

    # Only insert the roles if they do not exist
    if admin_role is None:
        new_admin = Role(name='admin', description='Admin of the app')
        db.session.add(new_admin)

    if customer_role is None:
        new_customer = Role(name='customer', description='Customers')
        db.session.add(new_customer)

    if manager_role is None:
        new_manager = Role(name='manager', description='Managers')
        db.session.add(new_manager)

    db.session.commit()

    

def create_initial_admin():
    hashed_password = generate_password_hash('clevergirl')
    fs_uniquifier = str(uuid.uuid4())
    # Create the 'admin' user
    # Create the 'admin' user without roles argument
    new_admin = user_datastore.create_user(
        username='Clevergirl',
        email='me.clevergirl@gmail.com',
        password=hashed_password,
        active=True,
        address='Cosmos',
        phone_number='789797940',
        fs_uniquifier=fs_uniquifier
    )

    # Commit the 'admin' user to the database
    db.session.add(new_admin)
    db.session.commit()
    admin_role = user_datastore.find_role('admin')
    user_datastore.add_role_to_user(new_admin, admin_role)
    db.session.commit()

# users = {
#     'admin': {
#         'password': generate_password_hash('adminpassword'),  # Hashed password
#         'roles': ['admin']
#     },
#     'user': {
#         'password': generate_password_hash('userpassword'),  # Hashed password
#         'roles': ['user']
#     },
#     'manager': {
#         'password': generate_password_hash('managerpassword'),  # Hashed password
#         'roles': ['manager']
#     }
# }

def role_required(req_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            print(f"user_id: {user_id}")
            current_user = User.query.filter_by(id=user_id).first()
            print(f"current_user: {current_user}")
            print(f"current_user roles: {[role.name for role in current_user.roles] if current_user else None}")

            if current_user and any(role.name in req_roles for role in current_user.roles):
                return func(*args, **kwargs)
            else:
                return jsonify({'message': 'Unauthorized'}), 403

        return wrapper
    return decorator



@app.route('/protected', methods=['GET'])
@auth_required("token")
def protected_route():
    # Extract the token from the Authorization header
    token = request.headers.get('Authorization').split(' ')[1]

    try:
        # Verify and decode the token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        # Here, you can use the user_id to fetch user data from your database
        return jsonify(message=f'Authenticated as user {user_id}')
    
    except jwt.ExpiredSignatureError:
        print("expried")
        return jsonify(error='Token has expired', status_code=401)
    except jwt.InvalidTokenError:
        print("No token")
        return jsonify(error='Invalid token', status_code=401)

@auth_bp.route('/categories', methods=['GET'])
def get_categories_and_products():
    categories = Category.query.all()
    print(categories)
    categories_data = []
    for category in categories:
        category_data = {
            'id': category.id,
            'name': category.name,
            'products': []
        }

        for product in category.products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'stock': product.stock,
                'manufacture_date': product.manufacture_date.strftime('%Y-%m-%d'),
                'expiry_date': product.expiry_date.strftime('%Y-%m-%d'),
                'rate_per_unit': product.rate_per_unit,
                'current_stock': product.current_stock,
                'rating': product.rating,
                'feedback': product.feedback
            }
            category_data['products'].append(product_data)
            print(category_data)

        categories_data.append(category_data)

    return jsonify(categories=categories_data)

from application import TEMP_FOLDER  
@auth_bp.route('/register_user', methods=['POST'])
def register_user():
    try:
        data = request.form.get('data')
        file = request.files.get('file')
        print(file)
        # Parse JSON data
        json_data = json.loads(data)
        name = json_data.get('name')
        email = json_data.get('email')
        password = json_data.get('password')
        role_name = json_data.get('role_name')
        address = json_data.get('address')
        phone_number = json_data.get('phone_number')
        department = json_data.get('department')
        hashed_password = generate_password_hash(password)
        fs_uniquifier = str(uuid.uuid4())
        roles = user_datastore.find_role(role_name)
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            return jsonify({'message': 'User with this email already exists'}), 400
        elif not existing_user and file and role_name == 'manager':
            filename = secure_filename(file.filename)
            name_without_extension = os.path.splitext(filename)
            from application import TEMP_FOLDER
            print(name_without_extension[0])
            file.save(os.path.join(TEMP_FOLDER, filename))  # Use TEMP_FOLDER directly
        elif not existing_user and file and role_name == 'customer':
            filename = secure_filename(file.filename)
            name_without_extension = os.path.splitext(filename)
            print(name_without_extension[0])
            from application import UPLOAD_USER_PHOTOS_FOLDER
            file.save(os.path.join(UPLOAD_USER_PHOTOS_FOLDER, filename))
        else:
            filename = None  # Set filename to None if file is not present

        if role_name == 'manager':
            temp_manager = Temp_Manager(
                username=name,
                email=email,
                password=hashed_password,
                address=address,
                phone_number=phone_number,
                department=department,
                fs_uniquifier=fs_uniquifier,
                filename=filename
            )

            db.session.add(temp_manager)
            db.session.commit()

        else:
            user = user_datastore.create_user(
                username=name,
                email=email,
                password=hashed_password,
                address=address,
                phone_number=phone_number,
                department=department,
                filename=filename,
                fs_uniquifier=fs_uniquifier
            )
            db.session.add(user)
            db.session.commit()

            # Pass the role object (roles) instead of role name to add_role_to_user
            user_datastore.add_role_to_user(user, roles)
            db.session.commit()

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'User registration failed', 'details': 'Reason for failure'}), 500

    if role_name == 'manager':
        return jsonify({'message': "Request sent for admin's approval"})
    else:
        return jsonify({'message': 'Success'})



@auth_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'User deletion failed', 'details': str(e)}), 500


    
@auth_bp.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    admin = User.query.filter_by(email=email).first()
    if admin is None:
        return jsonify({'message': 'Email not found'}), 401
    admin_role = user_datastore.find_role('admin')
    if admin_role in admin.roles:
        if not check_password_hash(admin.password, password):
            return jsonify({'message': 'Invalid password'}), 401

        access_token = create_access_token(identity=admin.id)
        admin.last_login = datetime.utcnow()
        response_data = {
            'message': 'Login successful',
            'user_id': admin.id,
            'access_token': access_token
        }
        login_user(admin)
        from application.task import send_login_confirmation
        send_login_confirmation.delay(admin.id)
        return jsonify(response_data), 200
    else:
        return jsonify({'message': 'Access denied, user is not an admin'}), 401


@auth_bp.route('/login_customer', methods=['POST'])
def login_customer():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    customer = User.query.filter_by(email=email).first()
    if customer is None:
        return jsonify({'message': 'Email not found'}), 401

    customer_role = user_datastore.find_role('customer')
    if customer_role in customer.roles:
        if not check_password_hash(customer.password, password):
            return jsonify({'message': 'Invalid password'}), 401
        customer.last_login = datetime.utcnow()
        access_token = create_access_token(identity=customer.id)
        
        response_data = {
            'message': 'Login successful',
            'user_id': customer.id,
            'access_token': access_token
        }
        login_user(customer)
        from application.task import send_login_confirmation
        send_login_confirmation.delay(customer.id)
        return jsonify(response_data), 200
    else:
        return jsonify({'message': 'Access denied, user is not an admin'}), 401
    
@auth_bp.route('/login_manager', methods=['POST'])
def login_manager():
    try:
        data = request.get_json()
        email = data.get('email')
        login_password = data.get('password')

        manager = User.query.filter_by(email=email).first()
        if manager is None:
            return jsonify({'message': 'Email not found'}), 401

        manager_role = user_datastore.find_role('manager')
        if manager_role in manager.roles:
            if not check_password_hash(manager.password, login_password):
                return jsonify({'message': 'Invalid password'}), 401
            access_token = create_access_token(identity=manager.id)
            manager.last_login = datetime.utcnow()
            login_user(manager)

            response_data = {
                'message': 'Login successful',
                'user_id': manager.id,
                'access_token': access_token
            }
            login_user(manager)
            from application.task import send_login_confirmation
            send_login_confirmation.delay(manager.id)
            print(manager)
            return jsonify(response_data), 200
        else:
            return jsonify({'message': 'Access denied, user is not a manager'}), 401
    except Exception as e:
        print(f"An error occurred while logging in: {str(e)}")
        return jsonify({'message': 'An error occurred while logging in'}), 500




@app.route('/logout',methods=['POST'])
@jwt_required()  # Requires a valid JWT token
def logout():
    logout_user()
    return jsonify({"message": "Logout successfull"})

@auth_bp.route('/get_categories')
@jwt_required()
def get_categories():
    categories = Category.query.all()
    category_list = [{'category_name': category.name, 'id':category.id} for category in categories]
    return jsonify({'categories': category_list})
from datetime import datetime

@auth_bp.route('/add_item', methods=['POST'])
@jwt_required()
@role_required(["admin", "manager"])
def add_item():
    user = current_user
    
    formdata = request.form.get('data')
    file = request.files.get('file')
    data = json.loads(formdata)
    name = data.get("name")
    stock = data.get("stock")
    data_category = data.get("category_id")
    rate_per_unit = data.get("rate_per_unit")
    manufacture_date_str = data.get('manufacture_date')
    expiry_date_str = data.get('expiry_date')
    manufacture_date = datetime.strptime(manufacture_date_str, '%Y-%m-%d')
    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
    print(data_category)
    category = Category.query.filter_by(id=data_category).first()
    if file:
        try:
            # Save the file to the server
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_PRODUCT_PHOTOS_FOLDER'], filename)
            file.save(file_path)
            print("File saved successfully:", file_path)
        except Exception as e:
            print("Error saving file:", e)
            return jsonify({'message': 'Error saving file'}), 500

        # Extract the filename without extension
        name_without_extension = os.path.splitext(filename)[0]
        print(name_without_extension)
    # Query the Category based on its name
    

    if category:
        # If the category is found, create a new Product with the correct category_id
        new_item = Product(
            name=name,
            stock=stock,
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            rate_per_unit=rate_per_unit,
            current_stock=stock,
            rating=0.0,
            feedback='',
            photo_filename=filename if file else None  # Use the filename if file is present
        )

        db.session.add(new_item)
        new_item.category = category
        db.session.commit()

        return jsonify({'message': "Product added successfully"}), 201
    else:
        return jsonify({'message': 'Category not found'}), 404

@auth_bp.route('/add_category', methods=['POST'])
@jwt_required()
@role_required(["admin"])
def add_category():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    data = request.get_json()
    category_name = data.get('category_name')
    print(user)
    if not category_name:
        return jsonify({'message': 'Category name is required'}), 400  # Bad Request
    else:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()
        from application.permissions import Request_Category
        req_cateogry = Request_Category.query.filter_by(name=category_name).first()
        if req_cateogry:
            db.session.delete(req_cateogry)
            db.session.commit()
            
        return jsonify({'message': 'Category added successfully'}), 200  # OK         
    return jsonify({'message': 'An error occurred while adding the category'}), 500  # Internal Server Error

import os
from flask import current_app

@auth_bp.route('/delete_product/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin','manager'])
def delete_product(product_id):
    # with app.app_context():
    product = Product.query.filter_by(id=product_id).first()
    print(product)
    if product is None:
        return jsonify({'message':"Product not found"}), 404
    if product.photo_filename:
        from application import UPLOAD_PRODUCT_PHOTOS_FOLDER
        photo_path = os.path.join(current_app.config['UPLOAD_PRODUCT_PHOTOS_FOLDER'], product.photo_filename)
        if os.path.exists(photo_path):
            os.remove(photo_path)
            db.session.delete(product)
            db.session.commit()
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message':"Product deleted successfully"})
from flask import jsonify

@auth_bp.route('/update_category/<int:categoryID>', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def update_category(categoryID):
    print(categoryID)
    from application.permissions import Update_Category
    try:
        data = request.json
        update_name = data.get('name')
        requested_category = Update_Category.query.filter_by(id = categoryID)
        if requested_category:
            old_category = Category.query.filter_by(id = requested_category.category_id).first()
            old_category.name = update_name
            db.session.commit()
        else:
            return jsonify({"message": "Category not found"})



        return jsonify({"message": "Category updated successfully"})
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/update_category_admin/<int:categoryID>', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def update_category_admin(categoryID):
    print(categoryID)
    try:
        data = request.json
        update_name = data.get('name')
        requested_category = Category.query.filter_by(id = categoryID).first()
        if requested_category:
            requested_category.name = update_name
            db.session.commit()
        else:
            return jsonify({"message": "Category not found"})



        return jsonify({"message": "Category updated successfully"})
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/delete_category_admin/<int:categoryID>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_category_admin(categoryID):
    try:
        category_to_delete = Category.query.filter_by(id=categoryID).first()
        if not category_to_delete:
            return jsonify({'error': 'Category not found'}), 404

        db.session.delete(category_to_delete)
        db.session.commit()
        return jsonify({"message": "Category Deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500

    

from flask import jsonify

@auth_bp.route('/delete_category/<int:categoryID>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_category(categoryID):
    from application.permissions import Delete_Category_Request
    try:
        # Query the requested category
        requested_category = Delete_Category_Request.query.filter_by(id=categoryID).first()
        cat = Category.query.filter_by(id = categoryID).first()
        # Check if the requested category exists
        if not requested_category and not cat:
            return jsonify({"error": "Category not found"}), 404
        elif requested_category:
            # Delete the category
            db.session.delete(requested_category)
            db.session.commit()
        elif cat:
            db.session.delete(cat)
            db.session.commit()
        return jsonify({"message": "Category deleted successfully"})
    except Exception as e:
        # Handle exceptions, log the error, and return an appropriate response
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

app.static_folder = 'static'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import send_file, jsonify, request
import io

@auth_bp.route('/dashboard', methods=['POST'])
@jwt_required()
@role_required(['manager'])
def manager_dashboard():
    try:
        from application.report import generate_daily_purchase_bar_chart, daily_purchase_report, save_daily_purchase_csv, monthly_purchase_report, save_monthly_purchase_csv,generate_monthly_purchase_bar_chart
        data = request.get_json()
        selected_date = data.get('selected_date')
        print(selected_date)

        # Use selected_date to generate the daily purchase report
        daily_purchases = daily_purchase_report(selected_date)
        # Save the daily purchase report in CSV format
        csv_filename = r'C:\Users\umesh\OneDrive\Documents\Datascience\Diploma\MAD2\newproject\newbackend\application\csv_reports\selected_date.csv'
        save_daily_purchase_csv(daily_purchases, csv_filename)
        
        # Generate and save the bar chart
        bar_chart_image = generate_daily_purchase_bar_chart(daily_purchases)
        date_split = selected_date.split('-')
        str_month, str_year = date_split[1], date_split[0]
        month, year = map(int, [str_month, str_year])
        print(month, year)
        # month, year = selected_date.split('-')[1], selected_date.split('-')[0]
        monthly_purchases = monthly_purchase_report(month,year)
        # Save the monthly purchase report in CSV format
        
        csv_filename_monthly = r'C:\Users\umesh\OneDrive\Documents\Datascience\Diploma\MAD2\newproject\newbackend\application\csv_reports\month.csv'
        save_monthly_purchase_csv(monthly_purchases, csv_filename_monthly)

        # Generate and save the monthly bar chart
        bar_chart_image_monthly = generate_monthly_purchase_bar_chart(monthly_purchases)
        # Return the CSV file and bar chart image data to the frontend
        return jsonify({
            'message': 'Report generated successfully',
            'csv_data': csv_filename,  # Sending the path to the daily CSV file
            'bar_chart_image_daily': bar_chart_image,  # Sending base64 encoded daily image data
            'csv_data_monthly': csv_filename_monthly,  # Sending the path to the monthly CSV file
            'bar_chart_image_monthly': bar_chart_image_monthly  # Sending base64 encoded monthly image data
        })


    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred while generating the report'}), 500

