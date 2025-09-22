from flask import redirect, render_template, session
from functools import wraps


def valida(usuario, db):
    rows = db.execute("SELECT * FROM users WHERE username = ?", (usuario,)).fetchall()
    return len(rows) == 1




def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def mxn(value):
    """Format value as currency (MXN)."""
    return f"${value:,.2f}"


def rows_to_dict(rows):
    """
    Convierte una lista de sqlite3.Row en lista de dict.
    """
    return [dict(row) for row in rows] if rows else []
