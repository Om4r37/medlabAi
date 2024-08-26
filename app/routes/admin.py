from flask import Blueprint, render_template, request, redirect, flash, session
from app.database import db
from app.utils import admin_required
import datetime, app.stroke, app.heart_attack

current_year = datetime.datetime.now().year
bp = Blueprint("admin", __name__)


@bp.route("/fill", methods=["GET", "POST"])
@admin_required
def fill():
    appointment_id = request.args.get("id")
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
    db.execute("UPDATE stats SET value = value + 1 WHERE name = 'total_results';")
    db.execute(
        "UPDATE stats SET value = value - 1 WHERE name = 'current_appointments';"
    )
    user_id = db.execute(
        "SELECT user_id FROM appointments WHERE id = ?;", appointment_id
    )[0]["user_id"]
    user_info = db.execute("SELECT * FROM users WHERE id = ?;", user_id)[0]
    print(user_info)
    test_type = db.execute(
        "SELECT tests.name FROM appointments JOIN tests ON appointments.test_id = tests.id WHERE appointments.id = ?;",
        appointment_id,
    )[0]["name"]
    if test_type == "stroke":
        data = [
            user_info["gender"],
            current_year - user_info["birth_year"],
            1 if request.form.get("hypertension") == "on" else 0,
            user_info["heart_disease"],
            user_info["work"],
            request.form.get("glucose"),
            user_info["weight"] / ((user_info["height"] / 100) ** 2),
        ]
        prediction = app.stroke.predict(data)
    elif test_type == "heart attack":
        data = [
            current_year - user_info["birth_year"],
            "M" if user_info["gender"] == 1 else "F",
            request.form.get("chest_pain"),
            request.form.get("blood_pressure"),
            request.form.get("cholesterol"),
            1 if int(request.form.get("fasting_blood_sugar")) > 120 else 0,
            request.form.get("resting_ECG"),
            request.form.get("max_heart_rate"),
            "Y" if user_info["exng"] == 1 else "N",
            request.form.get("oldpeak"),
            request.form.get("slope"),
        ]
        prediction = app.heart_attack.predict(data)
    db.execute(
        "INSERT INTO results_fields (appointment_id, name, value) VALUES (?, ?, ?);",
        appointment_id,
        "classification",
        str(prediction),
    )
    flash("Results recorded successfully!")
    return redirect("/results")


@bp.route("/user")
@admin_required
def user():
    tab = request.args.get("tab")
    user = db.execute("SELECT * FROM users WHERE id = ?;", request.args.get("id"))[0]
    return render_template("admin/user.jinja", user=user, tab=tab)


@bp.route("/users")
@admin_required
def users():
    users = db.execute("SELECT * FROM users;")[1:]
    return render_template(
        "admin/users.jinja", users=users, current_year=datetime.datetime.now().year
    )
