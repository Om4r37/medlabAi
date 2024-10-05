from flask import Blueprint, render_template,request, redirect, flash
from app import db
from app.models import Appointment, Location, Stats, Test
from app.utils import snake_case_to_title_case
from datetime import datetime, timedelta
from config import OPENING_TIME, CLOSING_TIME 
from flask_login import current_user, login_required
from sqlalchemy import func, update

bp = Blueprint("appointments", __name__)


# Eager load :load everything in one query if we need optimize the performance
'''
@bp.route("/appointments")
@login_required
def appointments():
    if current_user.is_admin:
        appointments = Appointment.query.options(
        joinedload(Appointment.user),
        joinedload(Appointment.location),
        joinedload(Appointment.test)
        ).all()
    else:
        appointments = Appointment.query.options(
        joinedload(Appointment.user),
        joinedload(Appointment.location),
        joinedload(Appointment.test)
        ).filter_by(user_id=current_user.id).all()

    return render_template(('admin' if current_user.is_admin else 'appointments') + "/appointments.jinja", appointments = appointments)

'''

# Lazy load :when you access for ex appointment.user additional query is made to fetch the user
@bp.route("/appointments", methods=["GET"])
@login_required
def appointments():
    if current_user.id == 1:
        appointments = Appointment.query.filter_by(is_done = False).all()
    else:
        appointments = Appointment.query.filter_by(is_done = False, user_id = current_user.id)   
    # there is no need for two templates :)    
    return render_template(('admin' if current_user.id == 1 else 'appointments') + "/appointments.jinja",
                            appointments = appointments)



@bp.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():
    if request.method == "GET":
        return render_template(
            "appointments/schedule.jinja",
             current_date = str(datetime.now())[:10],
            tests = Test.query.all(),
            locations = Location.query.all(),
            )
        
    # validate form inputs
    test_id = request.form.get("test")
    location_id = request.form.get("location")
    date = request.form.get("date")
    time = request.form.get("time")
        
    if not all([test_id, location_id, date, time]):
        return render_template("error.jinja", message="All fields are required", code= 400)
        
    test = Test.query.get( test_id )
    if not test:
        return render_template("error.jinja", message="Test not found.", code= 404)
        
    pre_requests = test.pre_requests
    missing = []

    for pre_request in pre_requests:
        # current_user.pre_request.name is None
        if getattr(current_user, pre_request.name) is None:
            missing.append(pre_request.name)

    if missing:
        return render_template("error.jinja",
                message=f"Missing prerequisites: {', '.join(map(snake_case_to_title_case,
                missing) )}", code=400)
    
    ex_appointment = Appointment.query.filter_by(time = 
                                                 f"{request.form.get('date')} {request.form.get('time')}").first()
    
    if ex_appointment:
        return render_template("error.jinja", message="Appointments already exist in this time", code= 400)

    appointment = Appointment(user_id = current_user.id,
                            test_id = test_id,
                            location_id = location_id,
                            time = f"{request.form.get("date")} {request.form.get("time")}"
                             )    
        
    db.session.add(appointment)

    stmt = (
        update(Stats)
        .where(Stats.name == 'current_appointments')
        .values(value = Stats.value + 1)
        )
    
    db.session.execute(stmt)
    db.session.commit()
    flash("Appointment scheduled successfully!")
    return redirect("/appointments")



@bp.route("/periods", methods=["GET"])
@login_required
def periods():
    try:
        date = request.args.get("date")
        if date == '':
            return "<option disabled>pick a day first</option>"
        
        location_id = request.args.get("location")
        test_id = request.args.get("test")

        if not all([test_id, location_id]):
            return render_template("error.jinja", message="All fields are required", code=400)

        test = Test.query.get(test_id)

        #test_name = test.name
        test_duration = test.duration

        # Convert opening and closing times to datetime objects
        opening_time = datetime.strptime(f"{date} {OPENING_TIME}", "%Y-%m-%d %H:%M")
        closing_time = datetime.strptime(f"{date} {CLOSING_TIME}", "%Y-%m-%d %H:%M")

        # Get existing appointments for the day
        existing_appointments = (
        db.session.query(Appointment)
        .filter_by(test_id= test_id, location_id= location_id, is_done= 0)
        .filter(func.date(Appointment.time) == date)
        .all()
    )

    
        booked_periods = set(appointment.time for appointment in existing_appointments)
        available_periods = []
        current_time = opening_time
        time_slot = timedelta(minutes= test_duration)

        while current_time + time_slot <= closing_time:
            if current_time.strftime("%Y-%m-%d %H:%M") not in booked_periods:
                available_periods.append(current_time.strftime("%H:%M"))
            current_time += time_slot

        return render_template("appointments/periods.jinja", periods= available_periods)
    
    except Exception as e:
        return render_template("error.jinja",message=f"An unexpected error occurred.", code=500), 500


# remove need to be POST or DELETE not GET request
@bp.route("/remove")
@login_required
def remove():
    try:
        appointment_id = request.args.get("id")
        appointment = Appointment.query.filter_by(id = appointment_id, user_id = current_user.id).first()

        if appointment:
            db.session.delete(appointment)
            stmt = (
                update(Stats)
                .where(Stats.name == 'current_appointments')
                .values(value = Stats.value - 1)
                )
            db.session.execute(stmt)
            db.session.commit()
            flash("Appointment removed successfully!")
            return redirect("/appointments")
        else:
            return render_template("error.jinja", message="Invalid Appointment.", code=500), 500
        

    except Exception as e:
        db.session.rollback()
        return render_template("error.jinja",message=f"An unexpected error occurred.", code=500), 500
    


    



   
    
    
