from amigo import errors
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(403)
def error_403(error):
    """Returns & renders a 403 error page.

    Args:
        error: The error to be handled.
    
    Returns:
        _render: A rendered page.
    """
    return render_template("errors/403.html"), 403


@errors.app_errorhandler(404)
def error_404(error):
    """Returns & renders a 404 error page.

    Args:
        error: The error to be handled.
    
    Returns:
        _render: A rendered page.
    """
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(500)
def error_500(error):
    """Returns & renders a 500 error page.

    Args:
        error: The error to be handled.
    
    Returns:
        _render: A rendered page.
    """
    return render_template("errors/500.html"), 500

@errors.route("/notfound")
def notfound():
    """Returns & renders a game not found page.

    Args:
        None
    
    Returns:
        _render: A rendered page.
    """
    return render_template("errors/game_not_found.html")