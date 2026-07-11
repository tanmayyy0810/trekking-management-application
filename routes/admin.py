from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from models.user import User
from models.trek import Trek
from models.booking import Booking

from flask import request
from datetime import datetime
from models import db
from models.staff_profile import StaffProfile

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard")
@login_required
def dashboard():

    if current_user.role != "admin":

        flash("Access Denied!", "danger")

        return redirect(url_for("home"))

    total_treks = Trek.query.count()

    total_users = User.query.filter_by(
        role="trekker"
    ).count()

    total_staff = User.query.filter_by(
        role="staff"
    ).count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings
    )

@admin.route("/admin/create-trek", methods=["GET", "POST"])
@login_required
def create_trek():

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":

        trek = Trek(
            trek_name=request.form["name"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            duration=int(request.form["duration"]),
            available_slots=int(request.form["slots"]),
            description=request.form["description"],
            start_date=datetime.strptime(
                request.form["start_date"],
                "%Y-%m-%d"
            ).date(),
            end_date=datetime.strptime(
                request.form["end_date"],
                "%Y-%m-%d"
            ).date(),
            status="Pending"
        )

        db.session.add(trek)
        db.session.commit()

        flash("Trek created successfully!", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template("admin/create_trek.html")

@admin.route("/admin/treks")
@login_required
def view_treks():

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    treks = Trek.query.order_by(Trek.id).all()

    return render_template(
        "admin/view_treks.html",
        treks=treks
    )

@admin.route("/admin/edit-trek/<int:trek_id>", methods=["GET", "POST"])
@login_required
def edit_trek(trek_id):

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    if request.method == "POST":

        trek.trek_name = request.form["name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = int(request.form["duration"])
        trek.available_slots = int(request.form["slots"])
        trek.description = request.form["description"]
        trek.status = request.form["status"]

        trek.start_date = datetime.strptime(
            request.form["start_date"],
            "%Y-%m-%d"
        ).date()

        trek.end_date = datetime.strptime(
            request.form["end_date"],
            "%Y-%m-%d"
        ).date()

        db.session.commit()

        flash("Trek updated successfully!", "success")

        return redirect(url_for("admin.view_treks"))

    return render_template(
        "admin/edit_trek.html",
        trek=trek
    )
@admin.route("/admin/delete-trek/<int:trek_id>")
@login_required
def delete_trek(trek_id):

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully!", "success")

    return redirect(url_for("admin.view_treks"))

@admin.route("/admin/manage-staff")
@login_required
def manage_staff():

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    staff_members = StaffProfile.query.all()

    return render_template(
        "admin/manage_staff.html",
        staff_members=staff_members
    )

@admin.route("/admin/approve-staff/<int:staff_id>")
@login_required
def approve_staff(staff_id):

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    staff = StaffProfile.query.get_or_404(staff_id)

    staff.approval_status = "Approved"

    db.session.commit()

    flash("Staff approved successfully!", "success")

    return redirect(url_for("admin.manage_staff"))
@admin.route("/admin/blacklist-staff/<int:staff_id>")
@login_required
def blacklist_staff(staff_id):

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    staff = StaffProfile.query.get_or_404(staff_id)

    staff.approval_status = "Blacklisted"

    staff.user.is_blacklisted = True

    db.session.commit()

    flash("Staff has been blacklisted successfully!", "success")

    return redirect(url_for("admin.manage_staff"))

@admin.route("/admin/assign-staff/<int:trek_id>", methods=["GET", "POST"])
@login_required
def assign_staff(trek_id):

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    approved_staff = StaffProfile.query.filter_by(
        approval_status="Approved"
    ).all()

    if request.method == "POST":

        staff_id = request.form["staff_id"]

        trek.assigned_staff_id = staff_id

        db.session.commit()

        flash("Staff assigned successfully!", "success")

        return redirect(url_for("admin.view_treks"))

    return render_template(
        "admin/assign_staff.html",
        trek=trek,
        staff_members=approved_staff
    )

@admin.route("/admin/manage-users")
@login_required
def manage_users():

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    users = User.query.filter_by(role="trekker").all()

    return render_template(
        "admin/manage_users.html",
        users=users
    )

@admin.route("/admin/blacklist-user/<int:user_id>")
@login_required
def blacklist_user(user_id):

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    user = User.query.get_or_404(user_id)

    user.is_blacklisted = True

    db.session.commit()

    flash("User blacklisted successfully!", "success")

    return redirect(url_for("admin.manage_users"))

@admin.route("/admin/bookings")
@login_required
def view_bookings():

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    bookings = Booking.query.all()

    return render_template(
        "admin/view_bookings.html",
        bookings=bookings
    )

@admin.route("/admin/search", methods=["GET", "POST"])
@login_required
def search():

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    results = []
    search_type = ""
    keyword = ""

    if request.method == "POST":

        search_type = request.form["search_type"]
        keyword = request.form["keyword"].strip()

        if search_type == "trek":

            if keyword.isdigit():
                results = Trek.query.filter_by(id=int(keyword)).all()
            else:
                results = Trek.query.filter(
                    Trek.trek_name.ilike(f"%{keyword}%")
                ).all()

        elif search_type == "staff":

            if keyword.isdigit():

                results = StaffProfile.query.join(User).filter(
                    User.id == int(keyword)
                ).all()

            else:

                results = StaffProfile.query.join(User).filter(
                    User.name.ilike(f"%{keyword}%")
                ).all()

        elif search_type == "user":

            if keyword.isdigit():

                results = User.query.filter_by(
                    id=int(keyword),
                    role="trekker"
                ).all()

            else:

                results = User.query.filter(
                    User.role == "trekker",
                    User.name.ilike(f"%{keyword}%")
                ).all()

    return render_template(
        "admin/search.html",
        results=results,
        search_type=search_type
    )
@admin.route("/admin/reactivate-staff/<int:staff_id>")
@login_required
def reactivate_staff(staff_id):

    if current_user.role != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    staff = User.query.get_or_404(staff_id)

    staff.is_blacklisted = False

    db.session.commit()

    flash("Staff reactivated successfully!", "success")

    return redirect(url_for("admin.manage_staff"))