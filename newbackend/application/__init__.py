from datetime import timedelta
from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from application.celery_worker import make_celery
from flask_caching import Cache

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisismysecretsecretkey'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)


UPLOAD_USER_PHOTOS_FOLDER = 'static/user_photos'  # Folder for user photos
UPLOAD_PRODUCT_PHOTOS_FOLDER = 'static/product_photos' 
TEMP_FOLDER = 'static/temp_folder'  

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_USER_PHOTOS_FOLDER'] = UPLOAD_USER_PHOTOS_FOLDER
app.config['UPLOAD_PRODUCT_PHOTOS_FOLDER'] = UPLOAD_PRODUCT_PHOTOS_FOLDER


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # SMTP server
app.config['MAIL_PORT'] = 587  # SMTP port (587 for TLS, 465 for SSL, 25 for non-secure)
app.config['MAIL_USE_TLS'] = True  # Use TLS (Transport Layer Security)
app.config['MAIL_USE_SSL'] = False  
app.config['MAIL_USERNAME'] = 'example@gmail.com' 
app.config['MAIL_PASSWORD'] = 'kjkjkjkjjljlj'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'example@gmail.com'  # Default sender
mail = Mail(app)

db = SQLAlchemy(app)





# Configure cache to use Redis
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_KEY_PREFIX'] = 'your_prefix_'
app.config['CACHE_REDIS_HOST'] = 'localhost'  # Update with your Redis server details
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0

# Create cache instance
cache = Cache(app)

# celery configuration
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    RESULT_BACKEND='redis://localhost:6379'
)



celery = make_celery(app)




from kombu import Exchange, Queue
CELERY_ENABLE_UTC = True  
 


CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

jwt = JWTManager(app)

from blueprint.auth import auth_bp, security,  user_datastore
from blueprint.user import user_bp
from blueprint.updates import updates_bp
from blueprint.requests import request_bp
from blueprint.ratings import rating_bp

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(updates_bp)
app.register_blueprint(request_bp)
app.register_blueprint(rating_bp)

from celery.schedules import crontab
CELERY_IMPORTS = ('application.task')
from application.task import send_daily_purchase_report, check_product_stock, send_inactive_customer_remainder

celery.conf.beat_schedule = {
    'send_daily_purchase_report': {
        'task': 'application.task.send_daily_purchase_report',
        'schedule': crontab(hour=7, minute=40),
    },
    'send-monthly-report': {
        'task': 'application.task.send_monthly_purchase_report_email',
        'schedule': crontab(day_of_month='1', hour=7, minute=40),
    },
    'check_product_stock':{
        'task': 'application.task.check_product_stock',
        'schedule': crontab(hour=7, minute=00),
    },
    'send_inactive_customer_remainder':{
        'task': 'application.task.send_inactive_customer_remainder',
        'schedule': crontab(hour=7, minute=00),
    }
}






