from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User
from models.staff_profile import StaffProfile
from models.trek import Trek
from models.booking import Booking
from routes.auth import auth
from flask import render_template
from routes.admin import admin
from routes.staff import staff
from routes.trekker import trekker


app = Flask(__name__)
app.config["SECRET_KEY"] = "trekking_management_secret_key"
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(staff)
app.register_blueprint(trekker)

@app.route("/")
def home():
    return render_template("home.html")



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
  

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(
            email="admin@gmail.com"
        ).first()

        if not admin:

            admin = User(
                name="Administrator",
                email="admin@gmail.com",
                role="admin"
            )

            admin.set_password("admin123")

            db.session.add(admin)
            db.session.commit()

            print("Default admin created.")

        print("Database created successfully!")

    app.run(debug=True)

  