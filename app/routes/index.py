from flask import Blueprint, redirect, render_template, request, flash
from flask_login import current_user, login_required
from sqlalchemy import  and_
from app import db
from datetime import datetime
from app.models import Appointment, ResultField, User


bp = Blueprint("index", __name__)
current_year = datetime.now().year


def dashboard():
    filters = {

    3: User.gender == 1,  # Male
    4: User.gender == 0,  # Female
    5: User.is_married == 1,  # Married
    6: User.smoke == 3,  # Current Smoker
    7: User.smoke == 2,  # Former Smoker
    8: User.smoke == 1,  # Never Smoked
    9: User.heart_disease == 1,  # Heart Disease
    10: User.exng == 1,  # Exercise Induced Angina (exng)
    11: User.residence == 0,  # Rural
    12: User.residence == 1,  # Urban
    13: User.work == 0,  # Never Worked
    14: User.work == 1,  # Private Work
    15: User.work == 2,  # Self Employed
    16: User.work == 3,  # Government Work
    17: User.work == 4,  # Children (Assuming this is a category)
    18: current_year - User.birth_year < 16,  # Age 0-15
    19: and_(current_year - User.birth_year > 15, current_year - User.birth_year < 31),  # Age 16-30
    20: and_(current_year - User.birth_year > 30, current_year - User.birth_year < 46),  # Age 31-45
    21: and_(current_year - User.birth_year > 45, current_year - User.birth_year < 61),  # Age 46-60
    22: and_(current_year - User.birth_year > 60, current_year - User.birth_year < 76),  # Age 61-75
    23: current_year - User.birth_year > 75,  # Age 76+
    }

    general_stats = {
    0: Appointment.query.count(),  
    1: ResultField.query.count(), 
    2: User.query.count() 
    }

    stats = {}
    stats.update(general_stats)  # add general_stats to stats

    for key, condition in filters.items():
        count = User.query.filter(condition).count()
        stats[key] = count 

    return render_template("admin/dashboard.jinja", stats = stats, user = current_user)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    try:
        if  request.method == "GET":
            if current_user.id == 1:
                return dashboard()
            
            return render_template(
                "index.jinja", user= current_user, current_year= current_year
            )
        

        for field in ("birth_year", "height", "weight","num_of_children","work", "smoke"):
            value = request.form.get(field)
            if value != None and value != "":
                try:
                    value = int(value)
                except ValueError:
                    return render_template("error.jinja", message="invalid " + field, code=400)
                
                # current_user.field = value
                setattr(current_user, field, value)


        for field in ("full_name", "email"):
            if value := request.form.get(field):
                setattr(current_user, field, value)

        for field in ("gender","is_married", "residence"):
            if value := request.form.get(field):
                setattr(current_user, field, 1)
           

        for field in ("exng", "heart_disease"):
            if value := request.form.get(field):
                setattr(current_user, field, 1)
            else:
                setattr(current_user, field, 0)

        db.session.commit()
        flash("Information Updated Successfully!")
        return redirect("/")
    
    except Exception as e:
        return render_template("error.jinja", message=f"An unexpected error occurred", code=500), 500


