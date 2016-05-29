import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = bool(os.environ.get('DEBUG') in ['yes', 1, 'true', 'True'])
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[gtfseditor]'
    FLASKY_MAIL_SENDER = 'Gtfseditor <gtfseditor@gmail.com>'

    AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@gtfseditor.com'

    FLASKY_SLOW_DB_QUERY_TIME=0.5

    BROKER_URL = os.environ.get('CLOUDAMQP_URL') or 'sqla+sqlite:///celerydb.sqlite'
    CELERY_RESULT_BACKEND = os.environ.get('CLOUDAMQP_URL') or 'db+sqlite:///celerydb.sqlite'
    TMP_FOLDER = '.tmp/'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class PostgresConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres:///gtfseditor'
    # SQLALCHEMY_ECHO = True

    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # log to stderr
        import logging
        from logging import getLogger
        from logging import StreamHandler
        from logging import FileHandler

        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.INFO)
        # app.logger.addHandler(stream_handler)

        # log to stderr
        file_handler = FileHandler('sql_log.log')
        file_handler.setLevel(logging.DEBUG)
        sql_logger = getLogger('sqlalchemy')
        sql_logger.addHandler(file_handler)

        # app_logger = app.logger
        # werkzeug_logger = getLogger('werkzeug')



class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.ADMIN_EMAIL],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'staging': PostgresConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': PostgresConfig
}
