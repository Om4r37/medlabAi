from flask import Blueprint, render_template, session, request
from app.database import db
from app.utils import login_required

bp = Blueprint("results", __name__)


@bp.route("/results")
@login_required
def results():
    query = """SELECT
    appointments.id,
    appointments.time,
    appointments.user_id,
    locations.name AS location,
    tests.name AS type,
    users.full_name AS name,
    users.username AS username
FROM appointments
JOIN users ON appointments.user_id = users.id
JOIN locations ON appointments.location_id = locations.id
JOIN tests ON appointments.test_id = tests.id
WHERE appointments.done = 1"""
    rows = (
        db.execute(query + ";")
        if session["user_id"] == 1
        else db.execute(query + " AND users.id = ?;", session["user_id"])
    )
    return render_template(("admin/" if session["user_id"] == 1 else "") + "results.jinja", rows=rows)


@bp.route("/result")
@login_required
def result():
    query = """SELECT results_fields.name, results_fields.value
FROM results_fields
JOIN appointments ON results_fields.appointment_id = appointments.id
WHERE appointments.id = ?"""
    rows = (
        db.execute(query + ";", request.args.get("id"))
        if session["user_id"] == 1
        else db.execute(
            query + " AND appointments.user_id = ?;",
            request.args.get("id"),
            session["user_id"],
        )
    )
    classification = render_template(f"results/{"" if rows[-1]["value"] == '0' else "ab"}normal.jinja") 
    return render_template(
        "results/result.jinja", rows=rows[:-1], classification=classification
    )
