from flask import Flask
from config import Config
from extensions import db, bcrypt
from models.user import User
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

    admin_exists = User.query.filter_by(role="admin").first()

    if not admin_exists:
        hashed_password = bcrypt.generate_password_hash("admin123").decode("utf-8")

        admin = User(
            email="admin@placementportal.com",
            password=hashed_password,
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully!")

app.register_blueprint(auth_bp, url_prefix="/auth")


@app.route("/")
def home():
    return {"message": "Placement Portal Backend Running"}

if __name__ == "__main__":
    app.run(debug=True)