from flask import Blueprint, render_template, session, request
from app.database import db
from app.utils import login_required
from datetime import datetime

bp = Blueprint("appointments", __name__)


@bp.route("/appointments")
@login_required
def appointments():
    rows = db.execute(
        "SELECT * FROM appointments WHERE user_id = ?",
        session["user_id"],
    )
    return render_template("appointments.jinja", rows=rows)


@bp.route("/appoint", methods=["GET", "POST"])
@login_required
def appoint():
    if request.method == "GET":
        return render_template(
            "appoint.jinja",
            current_date=str(datetime.now())[:10],
            types=db.execute("SELECT * FROM tests"),
            locations=db.execute("SELECT * FROM locations"),
        )
