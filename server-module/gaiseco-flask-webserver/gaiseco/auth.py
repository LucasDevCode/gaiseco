import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import current_app
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .utils import d
from .utils import start_first_thread
from .utils import check_first_thread_finish

from .utils import d

from .db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM Users WHERE user_id = ?", (user_id,)).fetchone()
        )
    
        """Check if thread is end"""

    # Toda vez que carregam uma página que precisa estar logado, 
    # é verificado se há alguma thread para rodar função em paralelo.
    d(current_app.config['THREADS'])
    
    start_first_thread()
    check_first_thread_finish()


@bp.route("/register", methods=("GET", "POST"))
@login_required
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        error = None
        category = None

        db = get_db()

        check_admin = db.execute(
            "SELECT g.role FROM Users u JOIN Groups g ON u.group_id = g.group_id WHERE u.user_id = ?",
            (session.get("user_id"),)
        ).fetchone()


        if check_admin[0] != 'admin':
            error = f"Only Admin can register new users."
            category = 'error'


        if not username:
            error = "Username is required."
            category = 'warning'
        elif not password:
            error = "Password is required."
            category = 'warning'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO Users (username, email, password, group_id) VALUES (?, ?, ?, ?)",
                    (username, email, generate_password_hash(password), 2),
                )
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered."
                category = 'error'
            else:
                # Success, go to the login page.
                return redirect(url_for("pages.index"))

        flash(error, category)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        category = None

        db = get_db()

        user = db.execute(
            "SELECT * FROM Users WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
            category = 'error'

        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."
            category = 'error'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["user_id"]

            return redirect(url_for("index"))

        flash(error, category)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
