from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from models.trek import Trek
from models.booking import Booking
from models import db

trekker = Blueprint("trekker", __name__)


@trekker.route("/trekker/dashboard")
@login_required
def dashboard():

    if current_user.role != "trekker":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    total_bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).count()

    available_treks = Trek.query.filter_by(status="Open").count()

    return render_template(
        "trekker/dashboard.html",
        total_bookings=total_bookings,
        available_treks=available_treks
    )
@trekker.route("/trekker/treks")
@login_required
def view_treks():

    if current_user.role != "trekker":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    treks = Trek.query.filter_by(status="Open").all()
    # treks = Trek.query.all()


    return render_template(
        "trekker/view_treks.html",
        treks=treks
    )

@trekker.route("/trekker/my-bookings")
@login_required
def my_bookings():

    if current_user.role != "trekker":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "trekker/my_bookings.html",
        bookings=bookings
    )

@trekker.route("/trekker/trek/<int:trek_id>")
@login_required
def trek_details(trek_id):

    if current_user.role != "trekker":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    return render_template(
        "trekker/trek_details.html",
        trek=trek
    )

@trekker.route("/trekker/book/<int:trek_id>")
@login_required
def book_trek(trek_id):

    if current_user.role != "trekker":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    # Trek must be open
    if trek.status != "Open":
        flash("This trek is not open for booking.", "danger")
        return redirect(url_for("trekker.view_treks"))

    # No slots available
    if trek.available_slots <= 0:
        flash("No slots available.", "danger")
        return redirect(url_for("trekker.view_treks"))

    # Already booked?
    existing = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id
    ).first()

    if existing:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("trekker.view_treks"))

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id,
        booking_status="Booked",
        payment_status="Pending"
    )

    db.session.add(booking)

    trek.available_slots -= 1

    db.session.commit()

    flash("Trek booked successfully!", "success")

    return redirect(url_for("trekker.my_bookings"))

@trekker.route("/trekker/cancel-booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):

    if current_user.role != "trekker":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    booking = Booking.query.get_or_404(booking_id)

    # Security check
    if booking.user_id != current_user.id:
        flash("Access Denied!", "danger")
        return redirect(url_for("trekker.my_bookings"))

    trek = booking.trek

    trek.available_slots += 1

    db.session.delete(booking)

    db.session.commit()

    flash("Booking cancelled successfully.", "success")

    return redirect(url_for("trekker.my_bookings"))