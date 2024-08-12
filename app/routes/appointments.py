from flask import Blueprint, render_template, session, request, redirect, flash
from app.database import db
from app.utils import login_required
from datetime import datetime, timedelta
from config import OPENING_TIME, CLOSING_TIME, TEST_TYPES

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
    flash("Appointment scheduled successfully!")
    return redirect("/appointments")


@bp.route("/periods")
@login_required
def periods():
    date = request.args.get("date")
    if date == '':
        return "<option disabled>pick a day first</option>"
    test_id = request.args.get("test")
    test_name = db.execute("SELECT name FROM tests WHERE id = ?", test_id)[0]['name']
    test_duration = TEST_TYPES[test_name]['duration']

    # Convert opening and closing times to datetime objects
    opening_time = datetime.strptime(f"{date} {OPENING_TIME}", "%Y-%m-%d %H:%M")
    closing_time = datetime.strptime(f"{date} {CLOSING_TIME}", "%Y-%m-%d %H:%M")

    # Get existing appointments for the day
    existing_appointments = db.execute(
        "SELECT time FROM appointments WHERE date(time) = ? AND test_id = ?",
        date,
        test_id
    )
    booked_periods = set(appointment['time'] for appointment in existing_appointments)

    available_periods = []
    current_time = opening_time
    time_slot = timedelta(minutes=test_duration)

    while current_time + time_slot <= closing_time:
        if current_time.strftime("%Y-%m-%d %H:%M") not in booked_periods:
            available_periods.append(current_time.strftime("%H:%M"))
        current_time += time_slot

    return render_template("appointments/periods.jinja", periods=available_periods)


@bp.route("/clear")
@login_required
def clear():
    db.execute("DELETE FROM appointments WHERE user_id = ?;", session["user_id"])
    flash("Appointments cleared successfully!")
    return redirect("/appointments")


@bp.route("/remove")
@login_required
def remove():
    db.execute(
        "DELETE FROM appointments WHERE id = ? AND user_id = ?;",
        request.args.get("id"),
        session["user_id"] # important to prevent users from deleting other users' appointments
    )
    flash("Appointment removed successfully!")
    return redirect("/appointments")
