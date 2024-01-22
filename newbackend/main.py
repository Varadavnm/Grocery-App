from application import app, db, user_datastore
from application.models import *
from application.permissions import *
from blueprint.auth import create_role, create_initial_admin, security
from flask_cors import CORS
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(email = 'me.clevergirl@gmail.com').first()
    if not admin:
        create_role()
        create_initial_admin()
if __name__ == '__main__':
    app.run(debug=True)

