from flask import Flask
from werkzeug.security import generate_password_hash
from application.routes import routes
from application.config import LocalDevelopmentConfig
from application.models import db, Admin
from asgiref.wsgi import WsgiToAsgi  # <-- Added wrapper import
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.register_blueprint(routes)
    print(app.url_map)
    return app

app = create_app()

# Wrap the WSGI app for ASGI server compatibility
asgi_app = WsgiToAsgi(app)  # <-- Added global wrapper variable

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

# This block is kept intact for local development purposes
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("app:asgi_app", host='0.0.0.0', port=port, log_level="info")