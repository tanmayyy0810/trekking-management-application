from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

staff = Blueprint("staff", __name__)


@staff.route("/staff/dashboard")
@login_required
def dashboard():

    if current_user.role != "staff":
        flash("Access Denied!", "danger")

        return redirect(url_for("home"))

    return render_template("staff/dashboard.html")