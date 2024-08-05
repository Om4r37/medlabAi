from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from datetime import datetime

current_year = datetime.now().year

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        user_info = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        user_info = user_info[0] if user_info else {}
        return render_template("index.html", user_info=user_info, current_year=current_year)

    for i in ("birth_year", "hight", "weight", "pregnancies"):
        value = request.form.get(i)
        if value != None and value != "":
            try:
                value = int(value)
            except ValueError:
                return render_template("error.html", message="invalid " + i, code=400)
            db.execute(
                "UPDATE users SET " + i + " = ? WHERE id = ?;",
                value,
                session["user_id"],
            )
    for i in ("full_name", "email"):
        value = request.form.get(i)
        if value:
            db.execute(
                "UPDATE users SET " + i + " = ? WHERE id = ?;",
                value,
                session["user_id"],
            )
    flash("Information Updated Successfully!")
    return redirect("/")


@app.route("/appointments")
@login_required
def appointments():
    return render_template("appointments.html")


@app.route("/results")
@login_required
def results():
    return render_template("results.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    verification = request.form.get("confirmation")

    if not username:
        return render_template("error.html", message="must provide username", code=400)

    if not password:
        return render_template("error.html", message="must provide password", code=400)

    if password != verification:
        return render_template("error.html", message="passwords don't match", code=400)

    if db.execute("SELECT * FROM users WHERE username = ?;", username):
        return render_template("error.html", message="username already taken", code=400)

    db.execute(
        "INSERT INTO users (username, hash) VALUES (?, ?);",
        username,
        generate_password_hash(password),
    )
    user = db.execute("SELECT * FROM users WHERE username = ?;", username)[0]
    session["user_id"] = user["id"]
    session["user_name"] = user["username"]
    flash("Account Created Successfully!")
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    # Ensure username was submitted
    if not request.form.get("username"):
        return render_template("error.html", message="must provide username", code=403)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return render_template("error.html", message="must provide password", code=403)

    # Query database for username
    rows = db.execute(
        "SELECT * FROM users WHERE username = ?;", request.form.get("username")
    )

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(
        rows[0]["hash"], request.form.get("password")
    ):
        return render_template(
            "error.html", message="invalid username and/or password", code=403
        )

    session["user_id"] = rows[0]["id"]
    session["user_name"] = rows[0]["username"]
    flash("Logged in as " + session["user_name"])
    return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message=str(e)[3:], code=404)


if __name__ == "__main__":
    app.run(debug=True)
