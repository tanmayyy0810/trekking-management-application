from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

trekker = Blueprint("trekker", __name__)


@trekker.route("/trekker/dashboard")
@login_required
def dashboard():

    if current_user.role != "trekker":
        flash("Access Denied!", "danger")

        return redirect(url_for("home"))

    return render_template("trekker/dashboard.html")