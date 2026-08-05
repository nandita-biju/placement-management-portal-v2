from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
cache = Cache()
mail = Mail()