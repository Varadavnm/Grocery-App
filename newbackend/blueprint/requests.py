import datetime
from functools import wraps
import celery
from jwt import ExpiredSignatureError, InvalidTokenError
# from flask.json import JSONEncoder
from flask import Flask, Blueprint, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, auth_required, login_required, roles_required, auth_token_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from application.models import User, Role, roles_users, Product, Category, Cart, Purchase
from application.permissions import Request_Category, Temp_Manager
from blueprint.auth import role_required, user_datastore
from flask_httpauth import HTTPTokenAuth
from flask_login import current_user  # Import current_user
from application import db, app
from flask_login import LoginManager, login_user, logout_user, login_remembered
from wtforms.validators import Email
import uuid

request_bp = Blueprint('requests', __name__)

@request_bp.route('/request_category',methods = ['GET','POST'])
@jwt_required()
def request_category():
    if request.method == 'GET':
        category_request = Request_Category.query.all()
        print(category_request)
        request_list = []
        for r in category_request:
            req = {
                'id' : r.id,
                'category_name': r.name,
                
            }
            print(r.name)
            request_list.append(req)
        return jsonify(category_requests = request_list)
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('category_name')
        cat_req = Request_Category(name=name)
        db.session.add(cat_req)
        db.session.commit()
        return jsonify({'message': 'Category request added successfully'})  
    return jsonify({'message': 'Something Went wrong'})
    
@request_bp.route('/update_category_request',methods = ['GET'])
@jwt_required()
@role_required(['admin'])
def update_category_request_get():
    from application.permissions import Update_Category
    update_requests = Update_Category.query.all()
    update_request_list = []
    update_request_list = [
        {'id':r.id,'name': r.name, 'category_id': r.category_id} for r in update_requests
    ]
    return jsonify(update_requests = update_request_list)

@request_bp.route('/update_category_request/<int:categoryId>',methods = ['POST'])
@jwt_required()
@role_required(['manager'])
def update_category_request_post(categoryId):
    print(categoryId)
    from application.permissions import Update_Category    
    old_category = Category.query.filter_by(id=categoryId).first()
    data = request.get_json()
    name = data.get('name')
    print(name)
    update_category = Update_Category(name=name, category_id = categoryId)
    db.session.add(update_category)
    db.session.commit()
    return jsonify({'message': 'Category update request sent to admin'})  

@request_bp.route('/delete_category_request/<int:categoryId>',methods = ['GET','POST'])
@jwt_required()
@role_required(['manager'])
def delete_category_request(categoryId):
    from application.permissions import Delete_Category_Request
    if request.method=='GET':
        delete_requests = Delete_Category_Request.query.all()
        delete_request_list = []
        for r in delete_requests:
            delete_request_list.append(r)
        return jsonify(delete_requests = delete_request_list)
    elif request.method=='POST':
        old_category = Category.query.filter_by(id=categoryId).first()
        data = request.get_json()
        name = data.get('name')
        delete_category_request = Delete_Category_Request(name=name, category_id = categoryId)
        db.session.add(delete_category_request)
        db.session.commmit()
    return jsonify({'message': 'Category update request sent to admin'})  



import os
import shutil


from application.task import send_approval_email
@request_bp.route('/add_manager', methods=['GET', 'POST'])
@jwt_required()
def add_manager():
    if request.method == 'GET':
        curr_managers = Temp_Manager.query.all()
        manager_list = []
        for manager in curr_managers:
            req = {
                'username': manager.username,
                'email': manager.email,
                'password': manager.password,  # Fix here
                'address': manager.address,
                'phone_number': manager.phone_number,
                'fs_uniquifier': manager.fs_uniquifier,
                'department': manager.department,
                'filename' : manager.filename
            }
            manager_list.append(req)
        return jsonify(managers=manager_list)

    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        address = data.get('address')
        phone_number = data.get('phone_number')
        fs_uniquifier = data.get('fs_uniquifier')
        department = data.get('department')
        filename = data.get('filename')
        print(filename)
        
        manager = user_datastore.create_user(
            username=username,
            email=email,
            password=password,
            address=address,
            phone_number=phone_number,
            department=department,
            filename=filename,
            fs_uniquifier=fs_uniquifier
        )
        db.session.commit()
        user_datastore.add_role_to_user(manager, 'manager')
        db.session.commit()
        print(email)
        from application.task import send_approval_email
        send_approval_email.delay(email)
        # Move the file from temporary folder to the final destination
        from application import TEMP_FOLDER, UPLOAD_USER_PHOTOS_FOLDER
        if filename:
            temp_folder_path = "static/temp_folder"
            file_path = os.path.join(temp_folder_path, filename)
            # Open the photo file in binary mode
            with open(file_path, 'rb') as photo_file:
                # Read the binary content of the photo file
                photo_data = photo_file.read()
            user_photos_folder = "static/user_photos"
            destination_file_path = os.path.join(user_photos_folder, filename)
            with open(destination_file_path, 'wb') as destination_file:
                # Write the binary content to the destination file
                destination_file.write(photo_data)
            temp_manager = Temp_Manager.query.filter_by(email=email).first()
            db.session.delete(temp_manager)
            db.session.commit()
            os.remove(file_path)
            return jsonify({'message': 'Manager added successfully'})
        temp_manager = Temp_Manager.query.filter_by(email=email).first()
        db.session.delete(temp_manager)
        db.session.commit()  
        return jsonify({'message': 'Manager added successfully'})

    return jsonify({'message': 'Invalid request'})
