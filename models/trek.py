from models import db


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    trek_name = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    difficulty = db.Column(db.String(20), nullable=False)

    duration = db.Column(db.Integer, nullable=False)

    available_slots = db.Column(db.Integer, nullable=False)

    description = db.Column(db.Text)

    start_date = db.Column(db.Date, nullable=False)

    end_date = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.String(20),
        default="Open"
    )

    assigned_staff_id = db.Column(
        db.Integer,
        db.ForeignKey("staff_profiles.id"),
        nullable=True
    )

    bookings = db.relationship(
        "Booking",
        backref="trek",
        lazy=True
    )

    def __repr__(self):
        return f"<Trek {self.trek_name}>"