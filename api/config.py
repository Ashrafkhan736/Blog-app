import os

# Add configration key for flask sqlalchemy model


class ModelConfigration():
    database_dir = os.path.dirname(__file__)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(database_dir, "blog.sqlite3")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = './static'
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    # CACHE_TYPE = "SimpleCache"  # Flask-Caching related configs
    # CACHE_DEFAULT_TIMEOUT = 60
    CACHE_TYPE = "RedisCache"  # Flask-Caching related configs
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 9    
    TIMEZONE='Asia/Kolkata'
class SecurityConfigration(ModelConfigration):
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", 'k3hkukVKksWfZWEKX5Gq417fYiNGZIvMTpdBsQ5MeJc')
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.environ.get(
        "SECURITY_PASSWORD_SALT", "215247499290732889899571631518337512956")
    SECURITY_TOKEN_AUTHENTICATION_KEY = "auth_token"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    WTF_CSRF_ENABLED = False
    # let user create new account
    SECURITY_REGISTERABLE = True
    