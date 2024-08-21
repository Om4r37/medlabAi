from flask import Flask, render_template
from flask_session import Session
from app.routes import auth, index, appointments, results, admin
from app.utils import snake_case_to_title_case, on2positive


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config.Config")

    # Register custom filters
    app.jinja_env.filters["snake_case_to_title_case"] = snake_case_to_title_case
    app.jinja_env.filters["on2positive"] = on2positive

    # Initialize session
    Session(app)

    # Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(appointments.bp)
    app.register_blueprint(results.bp)
    app.register_blueprint(admin.bp)

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.jinja", message=str(e)[3:], code=404)

    return app
