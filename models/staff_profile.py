from models import db



class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    phone = db.Column(db.String(15), nullable=False)

    experience = db.Column(db.Integer, default=0)

    approval_status = db.Column(
        db.String(20),
        default="Pending"
    )


    assigned_treks = db.relationship(
        "Trek",
        backref="staff",
        lazy=True
    )

    def __repr__(self):
        return f"<StaffProfile {self.user.name}>"