from flask import Blueprint, redirect, render_template, request, session, flash
from app.database import db
from datetime import datetime
from app.utils import login_required

bp = Blueprint("index", __name__)
current_year = datetime.now().year


def dashboard():
    stats = db.execute("SELECT * FROM stats;")
    query = "SELECT COUNT(*) FROM users WHERE "
    params = {
        3: "gender = 1",
        4: "gender = 0",
        5: "married = 1",
        6: "smoke = 3",
        7: "smoke = 2",
        8: "smoke = 1",
        9: "heart_disease = 1",
        10: "exng = 1",
        11: "residence = 0",
        12: "residence = 1",
        13: "work = 0",
        14: "work = 1",
        15: "work = 2",
        16: "work = 3",
        17: "work = 4",
        18: f"{current_year} - birth_year < 16",
        19: f"{current_year} - birth_year > 15 AND {current_year} - birth_year < 31",
        20: f"{current_year} - birth_year > 30 AND {current_year} - birth_year < 46",
        21: f"{current_year} - birth_year > 45 AND {current_year} - birth_year < 61",
        22: f"{current_year} - birth_year > 60 AND {current_year} - birth_year < 76",
        23: f"{current_year} - birth_year > 75",
    }

    for k, v in params.items():
        stats[k]["value"] = db.execute(query + v + ";")[0]["COUNT(*)"]

    return render_template("admin/dashboard.jinja", stats=stats)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        if session["user_id"] == 1:
            return dashboard()
        user_info = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        user_info = user_info[0] if user_info else {}
        return render_template(
            "index.jinja", user_info=user_info, current_year=current_year
        )

    for i in ("birth_year", "height", "weight", "pregnancies"):
        value = request.form.get(i)
        if value != None and value != "":
            try:
                value = int(value)
            except ValueError:
                return render_template("error.jinja", message="invalid " + i, code=400)
            db.execute(
                "UPDATE users SET ? = ? WHERE id = ?;",
                i,
                value,
                session["user_id"],
            )
    for i in ("full_name", "email"):
        if value := request.form.get(i):
            db.execute(
                "UPDATE users SET ? = ? WHERE id = ?;",
                i,
                value,
                session["user_id"],
            )
    for i in ("gender", "married", "residence"):
        if v := request.form.get(i):
            db.execute(
                "UPDATE users SET ? = ? WHERE id = ?;", i, v == "1", session["user_id"]
            )
    for i in ("exng", "heart_disease"):
        db.execute(
            "UPDATE users SET ? = ? WHERE id = ?;",
            i,
            1 if request.form.get(i) else 0,
            session["user_id"],
        )
    for i in ("work", "smoke"):
        db.execute(
            "UPDATE users SET ? = ? WHERE id = ?;",
            i,
            request.form.get(i),
            session["user_id"],
        )
    flash("Information Updated Successfully!")
    return redirect("/")


@bp.route("/delete")
@login_required
def delete():
    db.execute(
        "UPDATE users SET (full_name, email, gender, married, residence, birth_year, height, weight, pregnancies, exng, heart_disease, work, smoke) = (NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL) WHERE id = ?;",
        session["user_id"],
    )
    flash("User Data Deleted!")
    return redirect("/")
