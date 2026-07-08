from app import app
from models.user import User

with app.app_context():

    admin = User.query.filter_by(role="admin").first()

    if admin:
        print("Admin Found")
        print("Name :", admin.name)
        print("Email:", admin.email)
        print("Role :", admin.role)

    else:
        print("Admin not found")