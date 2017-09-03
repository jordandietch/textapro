import os
import sys
from flask_sqlalchemy import SQLAlchemy

# Set Path
pwd = os.path.abspath(os.path.dirname(__file__))
project = os.path.basename(pwd)
new_path = pwd.strip(project)
activate_this = os.path.join(new_path, 'app')
sys.path.append(activate_this)

from app import app, db
from models import Lead


def before_feature(context, feature):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    context.db = db
    context.db.create_all()
    context.client = app.test_client()


def after_feature(context, feature):
    db.drop_all()
