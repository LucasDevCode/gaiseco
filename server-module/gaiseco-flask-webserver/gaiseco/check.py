from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
import json

from .email import send_email
from .utils import d

import sys
sys.path.append('./analyzer')
import presidio_checker

from .auth import login_required
from .db import get_db

bp = Blueprint("check", __name__)


@bp.route("/check", methods=("POST",))
def check():
    """Check prompt."""
    if request.method == "POST":
        data = request.json

        ip = request.access_route[0]

        obj = None
        with open(file='config.json', mode='r') as f:
            obj = json.load( f )

        print(data)



        list_issues, text_issues_location = presidio_checker.check_prompt(text=data["prompt"], score_threshold=obj["score"]/100)
        
        d(list_issues)
        d(text_issues_location)

        if len(list_issues) > 0:
            db = get_db()

            db.execute(
                "INSERT INTO Prompts (employee_ip, model, session, employee_name, prompt, issue, minimum_score) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    ip, 
                    data['model'], 
                    data['session'],  
                    data['employee'], 
                    data['prompt'],
                    text_issues_location,
                    obj["score"]/100
                ),
            )
            
            db.commit()

            # d(list_issues)
            # d(text_issues_location)

            query = db.execute(
                "SELECT u.email FROM Users u INNER JOIN Groups g ON u.group_id = g.group_id WHERE g.role = 'manager'"
            ).fetchall()

            list_email_receiver = [ item[0] for item in query ]

            send_email(
                receivers_email=list_email_receiver, 
                employee=data['employee'], 
                original_prompt=data['prompt'], 
                marked_prompt=text_issues_location, 
                list_issues=list_issues
            )

    return json.dumps(True)
