from flask import Blueprint, redirect, render_template, request, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    try:
        if current_user.is_authenticated:
            return redirect('/')

        if request.method == "GET":
            return render_template("auth/register.jinja")

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        verification = request.form.get("confirmation")

        if not fullname:
            return render_template("error.jinja", message="must provide fullrname", code=400)
        
        if not email:
            return render_template("error.jinja", message="email provide password", code=400)

        if not password:
            return render_template("error.jinja", message="must provide password", code=400)

        if password != verification:
            return render_template("error.jinja", message="passwords don't match", code=400)
        

        exsisting_user = User.query.filter_by(email = email).first()
        # this msg could be changed for security concern
        if exsisting_user:
            return render_template(
                "error.jinja", message="Account Already exist", code=400
            )
        
        hashed_password = generate_password_hash(password)

        user = User(fullname= fullname, email= email, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account Created Successfully!")
        return redirect("/")
    
    except Exception as e:
        return render_template("error.jinja", message=f"An unexpected error occurred", code=500), 500
    




'''
@bp.route("/change_password", methods=["GET", "POST"])
def change_password():
    """Change user password"""
    if request.method == "GET":
        return render_template("auth/change_password.jinja")

    password = request.form.get("password")
    verification = request.form.get("confirmation")

    if not password:
        return render_template(
            "error.jinja", message="must provide new password", code=400
        )

    if password != verification:
        return render_template("error.jinja", message="passwords don't match", code=400)

    db.execute(
        "UPDATE users SET hash = ? WHERE id = ?;",
        generate_password_hash(password),
        session["user_id"],
    )
    flash("Password Changed Successfully!")
    return redirect("/")
'''



@bp.route("/login", methods=["GET", "POST"])
def login():
    try:
        if current_user.is_authenticated:
            return redirect('/')

        if request.method == "GET":
            return render_template("auth/login.jinja")
        
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            return render_template("error.jinja", message="must provide email", code=403)

        if not password:
            return render_template("error.jinja", message="must provide password", code=403)
        
        user = User.query.filter_by(email = email).first()

        if user and check_password_hash(user.password, password):
            login_user(user) 
            return redirect("/")
    
        flash("Invalid email or password")
        return render_template("auth/login.jinja")
    
    except Exception as e:
        return render_template("error.jinja", message=f"An unexpected error occurred", code=500), 500
        

@bp.route("/logout")
def logout():
    try:
        logout_user()
        return redirect("/login")
    
    except Exception as e:
        return render_template("error.jinja", message="An unexpected error occurred", code=500), 500
