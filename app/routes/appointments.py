from flask import Blueprint, render_template
from app.database import db
from app.utils import login_required

bp = Blueprint("appointments", __name__)


@bp.route("/appointments")
@login_required
def appointments():
    return render_template("appointments.jinja")
