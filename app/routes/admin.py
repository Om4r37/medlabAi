from flask import Blueprint, render_template, request, redirect, flash
from app import db
from app.utils import admin_required, classify
import datetime
from app.models import User, Appointment, ResultField
current_year = datetime.datetime.now().year
bp = Blueprint("admin", __name__)


@bp.route("/fill", methods=["GET", "POST"])
@admin_required
def fill():
   
  appointment_id = request.args.get("id")

  if request.method == "GET":
    appointment = Appointment.query.get(appointment_id)
    if appointment:
      test_type = appointment.test.name
      return render_template(f"admin/tests/{test_type}.jinja", id=appointment_id)
    else:
      flash("No test found for the given appointment ID")
      return redirect("/")

  # we need check that all items is insterted in form
  for field_name, field_value in request.form.items():
    result = ResultField(
            appointment_id= appointment_id,
            name= field_name,
            value= field_value,
          )
    db.session.add(result)

    # Mark appointment as done
  appointment = Appointment.query.get(appointment_id)
  appointment.is_done = True

  """
    # Update statistics
    stats_total_results = Stats.query.filter_by(name="total_results").first()
    stats_total_results.value += 1
    stats_current_appointments = Stats.query.filter_by(name="current_appointments").first()
    stats_current_appointments.value -= 1
  """

  classify(appointment_id)
  db.session.commit()
  flash("Results recorded successfully!")
  return redirect("/result?id=" + appointment_id)


@bp.route("/user")
@admin_required
def user():
    user_id = request.args.get("id")
    user = User.query.get(user_id)
    return render_template("admin/user.jinja", user= user)


@bp.route("/users")
@admin_required
def users():
    users = User.query.all()[1:] # Assuming you're skipping the first user for some reason :)
    return render_template("admin/users.jinja", users=users, current_year=datetime.datetime.now().year)


@bp.route("/invert")
@admin_required
def invert():
    appointment_id = request.args.get("id")
    result_field = ResultField.query.filter_by(
        name="classification", appointment_id=appointment_id
    ).first()
    result_field.value = 1 - int(result_field.value)  # toggle between 0 and 1
    db.session.commit()
    return redirect(f"/result?id={appointment_id}")
