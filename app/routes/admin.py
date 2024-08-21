from flask import Blueprint, render_template, request, redirect, flash
from app.database import db
from app.utils import admin_required

bp = Blueprint("admin", __name__)


@bp.route("/fill", methods=["GET", "POST"])
@admin_required
def fill():
    appointment_id = request.args.get("id")
    print(f"appointment_id: {appointment_id}")
    if request.method == "GET":
        type = db.execute(
            "SELECT tests.name FROM appointments JOIN tests ON appointments.test_id = tests.id WHERE appointments.id = ?;",
            appointment_id,
        )[0]["name"]
        return render_template(f"admin/tests/{type}.jinja", id=appointment_id)
    for i, v in request.form.items():
        db.execute(
            "INSERT INTO results_fields (appointment_id, name, value) VALUES (?, ?, ?);",
            appointment_id,
            i,
            v,
        )
    db.execute("UPDATE appointments SET done = true WHERE id = ?;", appointment_id)
    flash("Results recorded successfully!")
    return redirect("/results")


@bp.route("/user")
@admin_required
def user():
    user = db.execute("SELECT * FROM users WHERE id = ?;", request.args.get("id"))[0]
    return render_template("admin/user.jinja", user=user)
