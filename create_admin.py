from app import app
from models import db
from models.user import User

ADMIN_NAME = "Admin"
ADMIN_EMAIL = "admin@trek.com"
ADMIN_PASSWORD = "admin123"

with app.app_context():

    admin = User.query.filter_by(email=ADMIN_EMAIL).first()

    if admin:
        print("Admin already exists.")

    else:
        admin = User(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            role="admin"
        )

        admin.set_password(ADMIN_PASSWORD)

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")