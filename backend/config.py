import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "placement_portal.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "your-secret-key"
    JWT_SECRET_KEY = "this-is-a-very-secure-secret-key-for-placement-portal-project"

    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/0"
    
    # Flask-Caching
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = "placementportal217@gmail.com"
    MAIL_PASSWORD = "xbsr cwji kcro teve"

    MAIL_DEFAULT_SENDER = "placementportal217@gmail.com"