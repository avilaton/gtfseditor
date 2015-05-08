from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from config import config
from flask.ext.login import LoginManager
from flask_mail import Mail
from flask.ext.bootstrap import Bootstrap
from flask.ext.compress import Compress
from celery import Celery

db = SQLAlchemy()
mail = Mail()
cors = CORS()
compress = Compress()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    compress.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    app.config['CORS_HEADERS'] = 'X-Requested-With, Content-Type'
    cors.init_app(app)

    # if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    #     from flask.ext.sslify import SSLify
    #     sslify = SSLify(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .admin import admin as admin_blueprint
    if app.config['DEBUG']:
        admin_blueprint.static_folder = 'client/app'

    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .reports import reports as reports_blueprint
    app.register_blueprint(reports_blueprint, url_prefix='/reports')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app

def create_celery_app(app=None):
    app = app or create_app('staging')
    celery = Celery(__name__)
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery
