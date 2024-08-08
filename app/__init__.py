from flask import Flask
from flask_session import Session
from app.routes import auth, index, appointments, results


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config.Config")

    # Initialize session
    Session(app)

    # Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(appointments.bp)
    app.register_blueprint(results.bp)

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    return app
