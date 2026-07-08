from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.user import User
from models.staff_profile import StaffProfile
from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__)


# ---------------- Home Pages ----------------

@auth.route("/login")
def choose_login():
    return render_template("auth/choose_login.html")


@auth.route("/register")
def choose_register():
    return render_template("auth/choose_register.html")


# ---------------- Login Pages ----------------

@auth.route("/login/admin", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        admin = User.query.filter_by(
            email=email,
            role="admin"
        ).first()

        if admin and admin.check_password(password):

            login_user(admin)

            flash("Welcome Admin!", "success")

            return redirect(url_for("admin.dashboard"))   # Permanent

        flash("Invalid admin credentials.", "danger")

    return render_template("auth/admin_login.html")


@auth.route("/login/staff", methods=["GET", "POST"])
def staff_login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(
            email=email,
            role="staff"
        ).first()

        if user and user.check_password(password):

            profile = StaffProfile.query.filter_by(
                user_id=user.id
            ).first()

            if profile.approval_status != "Approved":

                flash(
                    "Your account is awaiting Admin approval.",
                    "warning"
                )

                return redirect(url_for("auth.staff_login"))

            login_user(user)

            flash("Login successful.", "success")

            return redirect(url_for("staff.dashboard"))   # permanent

        flash("Invalid email or password.", "danger")

    return render_template("auth/staff_login.html")


@auth.route("/login/trekker", methods=["GET", "POST"])
def trekker_login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        user = User.query.filter_by(

            email=email,

            role="trekker"

        ).first()

        if user and user.check_password(password):

            login_user(user)

            flash("Welcome! Login successful.", "success")

            return redirect(url_for("trekker.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/trekker_login.html")


# ---------------- Register Pages ----------------

@auth.route("/register/staff", methods=["GET", "POST"])
def staff_register():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()

        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Password validation
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.staff_register"))

        # Email already exists
        existing = User.query.filter_by(email=email).first()

        if existing:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.staff_register"))

        # Create User
        user = User(
            name=name,
            email=email,
            role="staff"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Create Staff Profile
        profile = StaffProfile(
            user_id=user.id,
            phone=phone
        )

        db.session.add(profile)
        db.session.commit()

        flash(
            "Registration successful. Your account is pending Admin approval.",
            "success"
        )

        return redirect(url_for("auth.staff_login"))

    return render_template("auth/staff_register.html")


@auth.route("/register/trekker", methods=["GET", "POST"])
def trekker_register():

    if request.method == "POST":

        name = request.form["name"].strip()

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            flash("Passwords do not match.", "danger")

            return redirect(url_for("auth.trekker_register"))

        existing = User.query.filter_by(email=email).first()

        if existing:

            flash("Email already registered.", "danger")

            return redirect(url_for("auth.trekker_register"))

        user = User(

            name=name,

            email=email,

            role="trekker"

        )

        user.set_password(password)

        db.session.add(user)

        db.session.commit()

        flash("Registration successful. Please login.", "success")

        return redirect(url_for("auth.trekker_login"))

    return render_template("auth/trekker_register.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out successfully.", "success")

    return redirect(url_for("home"))