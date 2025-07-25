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
from werkzeug.utils import secure_filename
from threading import Thread
import os
import json
import shutil

import sys
sys.path.append('./analyzer')
import pdf_extractor


from .utils import d
from .utils import start_first_thread
from .utils import check_first_thread_finish

from .auth import login_required
from .db import get_db

bp = Blueprint("config", __name__)


@bp.route('/config', methods=("GET","POST"))
@login_required
def index():
    """Check if thread is end"""
    start_first_thread()
    check_first_thread_finish()

    d(current_app.config['THREADS'])

    if request.method == "GET":
        """Show all the posts, most recent first."""
        db = get_db()

        users = db.execute(
            "SELECT user_id, username, email, group_id FROM Users"
        ).fetchall()

        groups = db.execute(
            "SELECT * FROM Groups"
        ).fetchall()

        obj = None
        with open(file='config.json', mode='r') as f:
            obj = json.load( f )

        list_files = os.listdir( current_app.config['UPLOAD_FOLDER'] )

        return render_template("config/index.html", score=obj["score"], users=users, groups=groups, list_files=list_files)
    elif request.method == "POST":
        score = int(request.form["input-number"])

        obj = None
        with open(file='config.json', mode='r') as f:
            obj = json.load( f )

        obj["score"] = score

        with open(file='config.json', mode='w') as f:
            json.dump(obj, f, indent=2)

        return redirect(url_for("config.index"))
        









def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'warning')
            return redirect(request.url)
        
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == '':
            flash('No selected file', 'warning')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            flash(f'Arquivo {filename} enviado!', 'success')

            # Call proccess PDF convert.
            if filename[ filename.rfind('.') : ] == '.pdf':
                t = Thread( 
                    target=pdf_extractor.pdf_to_txt_spacy, 
                    args=(
                        f"{current_app.config['UPLOAD_FOLDER']}/{filename}",    #pdf_path
                        f"{current_app.config['PROCESSED_FOLDER']}/{filename}", #txt_path
                        )
                )
                t.name = f'Processamento do arquivo {filename}'

                current_app.config['THREADS'].append( t )

            elif filename[ filename.rfind('.') : ] == '.txt':
                shutil.copyfile(
                    f"{current_app.config['UPLOAD_FOLDER']}/{filename}",    #pdf_path
                    f"{current_app.config['PROCESSED_FOLDER']}/{filename}"  #txt_path
                )


            # Call model training.
            t = Thread( 
                target=pdf_extractor.f1, 
                args=()
            )
            t.name = f'Treinamento do arquivo {filename} no modelo'

            current_app.config['THREADS'].append( t )


            t = Thread( 
                target=pdf_extractor.f2, 
                args=()
            )
            t.name = 'Pós treinamento'

            current_app.config['THREADS'].append( t )
            
            # # call proccess PDF convert.
            # pdf_extractor.pdf_to_txt_spacy(
            #     pdf_path=f"{current_app.config['UPLOAD_FOLDER']}/{filename}",
            #     txt_path=f"{current_app.config['PROCESSED_FOLDER']}/{filename}"
            # )

            return redirect(url_for('config.index'))
        
    return render_template("config/upload.html")
