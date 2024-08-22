from flask import Blueprint, redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("auth/register.jinja")

    username = request.form.get("username")
    password = request.form.get("password")
    verification = request.form.get("confirmation")

    if not username:
        return render_template("error.jinja", message="must provide username", code=400)

    if not password:
        return render_template("error.jinja", message="must provide password", code=400)

    if password != verification:
        return render_template("error.jinja", message="passwords don't match", code=400)

    if db.execute("SELECT * FROM users WHERE username = ?;", username):
        return render_template(
            "error.jinja", message="username already taken", code=400
        )

    db.execute(
        "INSERT INTO users (username, hash) VALUES (?, ?);",
        username,
        generate_password_hash(password),
    )
    user = db.execute("SELECT * FROM users WHERE username = ?;", username)[0]
    db.execute("UPDATE stats SET value = value + 1 WHERE name = 'users_count';")
    session["user_id"] = user["id"]
    session["user_name"] = user["username"]
    flash("Account Created Successfully!")
    return redirect("/")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()  # Forget any user_id

    if request.method == "GET":
        return render_template("auth/login.jinja")

    if not request.form.get("username"):
        return render_template("error.jinja", message="must provide username", code=403)

    if not request.form.get("password"):
        return render_template("error.jinja", message="must provide password", code=403)

    rows = db.execute(
        "SELECT * FROM users WHERE username = ?;", request.form.get("username")
    )

    if len(rows) != 1 or not check_password_hash(
        rows[0]["hash"], request.form.get("password")
    ):
        return render_template(
            "error.jinja", message="invalid username and/or password", code=403
        )

    session["user_id"] = rows[0]["id"]
    session["user_name"] = rows[0]["username"]
    flash("Logged in as " + session["user_name"])
    return redirect("/")


@bp.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")
