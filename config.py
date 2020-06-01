import os


class BaseConfig():
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATABASE_URL", "sqlite:///users.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = 'microservice'
    SEND_FILE_MAX_AGE_DEFAULT = 0


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
