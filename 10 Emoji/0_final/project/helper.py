from functools import wraps
from flask import redirect, render_template, session, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("You must be logged in to acces this route")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function