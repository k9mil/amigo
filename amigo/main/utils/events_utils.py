from functools import wraps
from flask import session, render_template

def access_required():
    """
    """
    def access_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "steam_id" in session:
                return func(*args, **kwargs)
            else:
                return render_template("index.html")
        return wrapper
    return access_decorator