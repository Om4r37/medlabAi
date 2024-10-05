from functools import wraps
from flask import redirect, render_template, request, session
import datetime

from flask_login import current_user
current_year = datetime.datetime.now().year
from app.AI  import diabetes_p, heart_attack, heart_failure, stroke
from app.models import Appointment, ResultField, Test, User
from app import db


#remove this
def login_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# modify this to check if user.is_admin == True
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return redirect("/")
        return f(*args, **kwargs)
    
    return decorated_function


def snake_case_to_title_case(snake_str):
    return " ".join([word[0].upper() + word[1:] for word in snake_str.split("_")])


def on2positive(str):
    return "Positive" if str == "On" else str



def calculate_bmi(user):
    return user.weight / ((user.height / 100) ** 2)


# this function need to be split for each test 
def classify(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    user = User.query.get(appointment.user_id)
    test = Test.query.get(appointment.test_id)
    test_type = test.name

    if test_type == "stroke":

        glucose = request.form.get("glucose")
        hypertension = request.form.get("hypertension")

        if not all([glucose, hypertension]):
            return render_template("error.jinja", message="All fields are required", code=400)

        data = [
            user.gender,
            current_year - user.birth_year,
            1 if hypertension == "on" else 0,
            user.heart_disease,
            user.work,
            glucose,
            calculate_bmi(user),
        ]
        prediction = stroke.predict(data)

    elif test_type == "heart attack":

        chest_pain = request.form.get("chest_pain")
        blood_pressure = request.form.get("blood_pressure")
        cholesterol = request.form.get("cholesterol")
        fasting_blood_sugar = request.form.get("fasting_blood_sugar")
        resting_ECG = request.form.get("resting_ECG")
        max_heart_rate = request.form.get("max_heart_rate")
        oldpeak = request.form.get("oldpeak")
        slope = request.form.get("slope")

        if not all([chest_pain, blood_pressure,cholesterol,fasting_blood_sugar,resting_ECG,
                    max_heart_rate,oldpeak,slope]):
            return render_template("error.jinja", message="All fields are required", code=400)

        data = [
            current_year - user.birth_year,
            "M" if user.gender == 1 else "F",
            chest_pain,
            blood_pressure,
            cholesterol,
            1 if int(fasting_blood_sugar) > 120 else 0,
            resting_ECG ,
            max_heart_rate,
            "Y" if user.exng == 1 else "N",
            oldpeak,
            slope,
        ]
        prediction = heart_attack.predict(data)


    elif test_type == "diabetes":

        glucose = request.form.get("glucose")
        blood_pressure = request.form.get("blood_pressure")
        skin_thickness = request.form.get("skin_thickness")
        insulin = request.form.get("insulin")
        pedigree = request.form.get("pedigree")

        if not all([glucose, blood_pressure,skin_thickness,insulin,pedigree]):
            return render_template("error.jinja", message="All fields are required", code=400)

        data = [
            user.num_of_children,  # Assuming this field represents pregnancies
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            calculate_bmi(user),
            pedigree,
            current_year - user.birth_year,
        ]
        prediction = diabetes_p.predict(data)


    elif test_type == "heart failure":

        anaemia = request.form.get("anaemia")
        creatinine_phosphokinase = request.form.get("creatinine_phosphokinase")
        diabetes = request.form.get("diabetes")
        ejection_fraction = request.form.get("ejection_fraction")
        high_blood_pressure = request.form.get("high_blood_pressure")
        platelets = request.form.get("platelets")
        serum_creatinine = request.form.get("serum_creatinine")
        serum_sodium = request.form.get("serum_sodium")

        if not all([anaemia,creatinine_phosphokinase,diabetes,ejection_fraction,high_blood_pressure,
                    platelets,serum_creatinine,serum_sodium]):
            return render_template("error.jinja", message="All fields are required", code=400)

        data = [
            current_year - user.birth_year,
            1 if anaemia == "on" else 0,
            creatinine_phosphokinase,
            1 if diabetes == "on" else 0,
            ejection_fraction,
            1 if high_blood_pressure  == "on" else 0,
            platelets,
            serum_creatinine,
            serum_sodium,
            user.gender,
            1 if user.smoke == 3 else 0,
            250,  # Assuming this is a fixed value  
        ]
        prediction = heart_failure.predict(data)

    # Insert the prediction result into the ResultField table
    result = ResultField(
        appointment_id=appointment_id,
        name="classification",
        value=str(prediction)
    )
   
    db.session.add(result)


    # if u want use this method dont forget to commit the changes
  

   