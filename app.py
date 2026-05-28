from flask import Flask
from werkzeug.security import generate_password_hash
from application.routes import routes
from application.config import LocalDevelopmentConfig
from application.models import db, Admin

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.register_blueprint(routes)
    print(app.url_map)
    return app

app = create_app()

with app.app_context():
    db.create_all()

    admin = Admin.query.filter_by(email="user0@admin.com").first()

    if not admin:
        admin = Admin(
            name="Admin",
            email="user0@admin.com",
            password=generate_password_hash("1234")
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")

    else:
        print("Admin already exists!")

if __name__ == "__main__":
    app.run(debug=True)