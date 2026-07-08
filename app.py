from flask import Flask
from config import Config
from models import db
from models.user import User
from models.staff_profile import StaffProfile
from models.trek import Trek
from models.booking import Booking

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def home():
    return "<h1>Welcome to Trekking Management Application</h1>"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database created successfully!")

    app.run(debug=True)