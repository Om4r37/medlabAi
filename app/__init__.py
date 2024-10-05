from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

def create_app():
    app = Flask(__name__)
    # Load configuration
    app.config.from_object("config.Config")
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.utils import snake_case_to_title_case, on2positive
   
    # Register custom filters
    app.jinja_env.filters["snake_case_to_title_case"] = snake_case_to_title_case
    app.jinja_env.filters["on2positive"] = on2positive

    from app.routes import auth, index, appointments, results, admin

    # Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(appointments.bp)
    app.register_blueprint(results.bp)
    app.register_blueprint(admin.bp)

    '''
    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
    '''

    '''
    # this code prevent full error msg from being shown 
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.jinja", message=str(e)[3:], code=404)
    '''

    from app.database import init_db
    
    with app.app_context():
    # Create the database if it doesn't exist
        db.create_all()
        init_db(db)

    return app
