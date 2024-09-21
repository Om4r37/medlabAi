from flask import Blueprint, render_template, request, redirect, flash, session
from app.database import db
from app.utils import admin_required
from app import stroke, heart_failure, heart_attack, diabetes
import datetime

current_year = datetime.datetime.now().year
bp = Blueprint("admin", __name__)


def classify(appointment_id):
    user_id = db.execute(
        "SELECT user_id FROM appointments WHERE id = ?;", appointment_id
    )[0]["user_id"]

    test_type = db.execute(
        "SELECT tests.name FROM appointments JOIN tests ON appointments.test_id = tests.id WHERE appointments.id = ?;",
        appointment_id,
    )[0]["name"]

    user_info = db.execute("SELECT * FROM users WHERE id = ?;", user_id)[0]

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
        prediction = stroke.predict(data)

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
        prediction = heart_attack.predict(data)
    elif test_type == "diabetes":
        data = [
            user_info["pregnancies"],
            request.form.get("glucose"),
            request.form.get("blood_pressure"),
            request.form.get("skin_thickness"),
            request.form.get("insulin"),
            user_info["weight"] / ((user_info["height"] / 100) ** 2),
            request.form.get("pedigree"),
            current_year - user_info["birth_year"],
        ]
        prediction = diabetes.predict(data)
    elif test_type == "heart failure":
        data = [
            current_year - user_info["birth_year"],
            1 if request.form.get("anaemia") == "on" else 0,
            request.form.get("creatinine_phosphokinase"),
            1 if request.form.get("diabetes") == "on" else 0,
            request.form.get("ejection_fraction"),
            1 if request.form.get("high_blood_pressure") == "on" else 0,
            request.form.get("platelets"),
            request.form.get("serum_creatinine"),
            request.form.get("serum_sodium"),
            user_info["gender"],
            1 if user_info["smoke"] == 3 else 0,
            250,
        ]
        prediction = heart_failure.predict(data)
    db.execute(
        "INSERT INTO results_fields (appointment_id, name, value) VALUES (?, ?, ?);",
        appointment_id,
        "classification",
        str(prediction),
    )


@bp.route("/fill", methods=["GET", "POST"])
def fill():
    appointment_id = request.args.get("id")
    if request.method == "GET":
        result = db.execute(
            "SELECT tests.name FROM appointments JOIN tests ON appointments.test_id = tests.id WHERE appointments.id = ?;",
            (appointment_id,),  # Pass as a tuple
        )
        
        if result:
            type = result[0]["name"]
            return render_template(f"admin/tests/{type}.jinja", id=appointment_id)
        else:
            flash("No test found for the given appointment ID.")
            return redirect("/")  

    for i, v in request.form.items():
        # the data need to be validated before insert into data base
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
    classify(appointment_id)
    flash("Results recorded successfully!")
    return redirect("/result?id=" + appointment_id)



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


@bp.route("/invert")
@admin_required
def invert():
    id = request.args.get("id")
    db.execute(
        "UPDATE results_fields SET value = 1 - value WHERE name = 'classification' AND appointment_id = ?;",
        id,
    )
    return redirect(f"/result?id={id}")
