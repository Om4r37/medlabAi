from flask import Blueprint, render_template
from app.database import db
from app.utils import login_required

bp = Blueprint("results", __name__)


@bp.route("/results")
@login_required
def results():
    return render_template("results.jinja")
