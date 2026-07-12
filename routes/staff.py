from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from models import db
from models.trek import Trek
from models.booking import Booking
from models.staff_profile import StaffProfile

staff = Blueprint("staff", __name__)


@staff.route("/staff/dashboard")
@login_required
def dashboard():

    if current_user.role != "staff":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    profile = StaffProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    assigned_treks = Trek.query.filter_by(
        assigned_staff_id=profile.id
    ).all()

    total_trekkers = Booking.query.join(Trek).filter(
        Trek.assigned_staff_id == profile.id,
        Booking.booking_status == "Booked"
    ).count()

    return render_template(
        "staff/dashboard.html",
        assigned_treks=assigned_treks,
        total_trekkers=total_trekkers
    )

@staff.route("/staff/profile", methods=["GET", "POST"])
@login_required
def profile():

    if current_user.role != "staff":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    profile = StaffProfile.query.filter_by(user_id=current_user.id).first()

    if request.method == "POST":

        current_user.name = request.form["name"]
        current_user.email = request.form["email"]
        profile.phone = request.form["phone"]
        profile.experience = request.form["experience"]

        db.session.commit()

        flash("Profile Updated Successfully.", "success")

        return redirect(url_for("staff.profile"))

    return render_template(
        "staff/profile.html",
        profile=profile
    )

@staff.route("/staff/update-slots/<int:trek_id>", methods=["GET", "POST"])
@login_required
def update_slots(trek_id):

    if current_user.role != "staff":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    # Ensure only assigned staff can edit
    if trek.assigned_staff_id != current_user.staff_profile.id:
        flash("You are not assigned to this trek.", "danger")
        return redirect(url_for("staff.dashboard"))

    if request.method == "POST":

        trek.available_slots = int(request.form["available_slots"])

        db.session.commit()

        flash("Available slots updated successfully.", "success")

        return redirect(url_for("staff.dashboard"))

    return render_template(
        "staff/update_slots.html",
        trek=trek
    )

@staff.route("/staff/update-status/<int:trek_id>", methods=["GET", "POST"])
@login_required
def update_status(trek_id):

    if current_user.role != "staff":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    # Only assigned staff can update
    if trek.assigned_staff_id != current_user.staff_profile.id:
        flash("You are not assigned to this trek.", "danger")
        return redirect(url_for("staff.dashboard"))

    if request.method == "POST":

        trek.status = request.form["status"]

        db.session.commit()

        flash("Trek status updated successfully.", "success")

        return redirect(url_for("staff.dashboard"))

    return render_template(
        "staff/update_status.html",
        trek=trek
    )

@staff.route("/staff/participants/<int:trek_id>")
@login_required
def view_participants(trek_id):

    if current_user.role != "staff":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    profile = StaffProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    trek = Trek.query.get_or_404(trek_id)

    # Ensure only assigned staff can view
    if trek.assigned_staff_id != profile.id:
        flash("You are not assigned to this trek.", "danger")
        return redirect(url_for("staff.dashboard"))

    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    return render_template(
        "staff/participants.html",
        trek=trek,
        bookings=bookings
    )

@staff.route("/staff/complete-booking/<int:booking_id>")
@login_required
def complete_booking(booking_id):

    if current_user.role != "staff":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    booking = Booking.query.get_or_404(booking_id)

    profile = StaffProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    if booking.trek.assigned_staff_id != profile.id:
        flash("You are not assigned to this trek.", "danger")
        return redirect(url_for("staff.dashboard"))

    booking.booking_status = "Completed"

    db.session.commit()

    flash("Participant marked as completed.", "success")

    return redirect(
        url_for(
            "staff.view_participants",
            trek_id=booking.trek.id
        )
    )

@staff.route("/staff/complete-payment/<int:booking_id>")
@login_required
def complete_payment(booking_id):

    if current_user.role != "staff":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    booking = Booking.query.get_or_404(booking_id)

    profile = StaffProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    # Ensure only assigned staff can update payment
    if booking.trek.assigned_staff_id != profile.id:
        flash("You are not assigned to this trek.", "danger")
        return redirect(url_for("staff.dashboard"))

    booking.payment_status = "Paid"

    db.session.commit()

    flash("Payment marked as completed.", "success")

    return redirect(
        url_for(
            "staff.view_participants",
            trek_id=booking.trek.id
        )
    )