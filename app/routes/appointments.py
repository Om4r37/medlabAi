from flask import Blueprint, render_template, session, request, redirect
from app.database import db
from app.utils import login_required
from datetime import datetime

bp = Blueprint("appointments", __name__)


@bp.route("/appointments")
@login_required
def appointments():
    rows = db.execute('''
SELECT
    appointments.id,
    appointments.time,
    locations.name AS location,
    tests.name AS type
FROM appointments
JOIN users ON appointments.user_id = users.id
JOIN locations ON appointments.location_id = locations.id
JOIN tests ON appointments.test_id = tests.id
WHERE users.id = ?;''',
        session["user_id"],
    )
    return render_template("appointments/appointments.jinja", rows=rows)


@bp.route("/appoint", methods=["GET", "POST"])
@login_required
def appoint():
    if request.method == "GET":
        return render_template(
            "appointments/appoint.jinja",
            current_date=str(datetime.now())[:10],
            tests=db.execute("SELECT * FROM tests"),
            locations=db.execute("SELECT * FROM locations"),
        )
    missing = []
    prerequisites = db.execute("SELECT name FROM prerequisites WHERE test_id = ?;", request.form.get("test"))
    for prerequisite in prerequisites:
        if db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])[0][prerequisite["name"]] == None:
            missing.append(prerequisite["name"])
    if missing:
        return render_template("error.jinja", message=f"Missing prerequisites: {', '.join(missing)}", code=400)
    db.execute(
        "INSERT INTO appointments (user_id, test_id, location_id, time) VALUES (?, ?, ?, ?);",
        session["user_id"],
        request.form.get("test"),
        request.form.get("location"),
        f"{request.form.get("date")} {request.form.get("time")}",
    )
    return redirect("/appointments")


@bp.route("/times")
@login_required
def times():
    date = request.args.get("date")
    return render_template("appointments/times.jinja")


@bp.route("/clear")
@login_required
def clear():
    db.execute("DELETE FROM appointments WHERE user_id = ?;", session["user_id"])
    return redirect("/appointments")


@bp.route("/remove")
@login_required
def remove():
    db.execute(
        "DELETE FROM appointments WHERE id = ? AND user_id = ?;",
        request.args.get("id"),
        session["user_id"] # important to prevent users from deleting other users' appointments
    )
    return redirect("/appointments")
