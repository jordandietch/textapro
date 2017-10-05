import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_ON = False
    MAIL_SERVER = 'smtp.mailgun.org'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_ADMIN = os.environ.get('MAIL_ADMIN')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    PHONE_ADMIN = os.environ.get('PHONE_ADMIN')
    TEST_PHONE = os.environ.get('TEST_PHONE')
    TWILIO_PHONE = os.environ.get('TWILIO_PHONE')

class ProductionConfig(Config):
    DEBUG = False
    MAIL_ON = True


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
