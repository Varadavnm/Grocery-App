from application.models import * 

#model for request new category
class Request_Category(db.Model):
    __tablename__ = 'request_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique = True)
    def __init__(self, name):
        self.name = name
class Update_Category(db.Model):
    __tablename__ = 'update_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(200), unique = True)
    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

class Delete_Category_Request(db.Model):
    __tablename__ = 'delete_category_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(200), unique = True)
    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

class Temp_Manager(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    filename = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(100), nullable=False) 
    phone_number = db.Column(db.String(20), nullable=False)  
    department = db.Column(db.String(100), nullable=True)
    active = True
    password = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    def __init__(self, username, email, password, address, phone_number, fs_uniquifier, filename=None, department=None):
        self.username = username
        self.email = email
        self.password = password
        self.address = address
        self.active = True
        self.phone_number = phone_number
        self.department = department
        self.fs_uniquifier = fs_uniquifier
        self.filename = filename
        