from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard")
@login_required
def dashboard():

    if current_user.role != "admin":

        flash("Access Denied!", "danger")

        return redirect(url_for("home"))

    return render_template("admin/dashboard.html")