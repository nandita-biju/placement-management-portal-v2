from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_mail import Mail

mail = Mail()

db = SQLAlchemy()
bcrypt = Bcrypt()

cache = Cache(config={
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://localhost:6379/0"
})