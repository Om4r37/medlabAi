from functools import wraps
from flask import redirect, session


def login_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") != 1:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function


def snake_case_to_title_case(snake_str):
    return " ".join([word.capitalize() for word in snake_str.split("_")])
