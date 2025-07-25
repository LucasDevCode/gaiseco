from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import send_from_directory
from flask import current_app
from werkzeug.exceptions import abort
import os

from .utils import d

from .auth import login_required
from .db import get_db

bp = Blueprint("pages", __name__)

@bp.route("/")
@login_required
def index():
    """Show all the posts, most recent first."""
    db = get_db()

    prompts_per_employee = db.execute(
        "SELECT COUNT(*) AS C, employee_name FROM Prompts GROUP BY employee_name ORDER BY C desc"
    ).fetchall()

    return render_template("pages/index.html", prompts_per_employee=prompts_per_employee)


@bp.route("/prompts")
@login_required
def prompts():
    """Show all the posts, most recent first."""
    db = get_db()
    prompts = db.execute(
        "SELECT * FROM Prompts ORDER BY timestamp desc"
    ).fetchall()

    tmp_path = current_app.config['TMP_FOLDER']

    # remove tmp files
    list_files = os.listdir(tmp_path)

    for file in list_files:
        os.remove( os.path.join(tmp_path, file) )
 
    # Salvar arquivos temporarios.
    for prompt in prompts:
        with open(file=f'{tmp_path}/prompt{prompt[0]}.txt', mode='w+') as f:
            f.write( prompt[5] )
            f.close()

        with open(file=f'{tmp_path}/issue{prompt[0]}.txt', mode='w+') as f:
            f.write( prompt[6] )
            f.close()        

    return render_template("pages/prompts.html", prompts=prompts)


