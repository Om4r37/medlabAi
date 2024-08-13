from flask import Blueprint, redirect, render_template, request, session, flash
from app.database import db
from datetime import datetime
from app.utils import login_required

bp = Blueprint("index", __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        if session["user_id"] == 1:
            return render_template("admin/dashboard.jinja")
        user_info = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        user_info = user_info[0] if user_info else {}
        return render_template(
            "index.jinja", user_info=user_info, current_year=datetime.now().year
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
    for i in (
        "full_name",
        "email",
        "gender",
        "married",
        "residence",
        "birth_year",
        "height",
        "weight",
        "pregnancies",
        "exng",
        "heart_disease",
        "work",
        "smoke",
    ):
        db.execute("UPDATE users SET ? = NULL WHERE id = ?;", i, session["user_id"])
    flash("User Data Deleted!")
    return redirect("/")
