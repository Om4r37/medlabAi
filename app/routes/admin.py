from flask import Blueprint, render_template, request
from app.database import db
from app.utils import admin_required

bp = Blueprint("admin", __name__)


@bp.route("/fill", methods=["GET", "POST"])
@admin_required
def fill():
    if request.method == "GET":
        return render_template("admin/fill.jinja")
