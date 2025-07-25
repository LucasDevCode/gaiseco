import os
import json

from flask import Flask

UPLOAD_FOLDER =    './gaiseco/static/files/upload'
PROCESSED_FOLDER = './gaiseco/static/files/processed'
TMP_FOLDER =       './gaiseco/static/tmp'
MODEL_FOLDER =     './gaiseco/static/model'

ALLOWED_EXTENSIONS = {'txt', 'pdf'}


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "gaiseco.sqlite"),
    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
    app.config['TMP_FOLDER'] = TMP_FOLDER
    app.config['MODEL_FOLDER'] = MODEL_FOLDER

    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

    app.config['THREADS'] = []

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile("config.py", silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"   
    
    @app.route("/ping")
    def ping():
        return json.dumps('pong')

    # register the database commands
    from . import db

    db.init_app(app)

    # apply the blueprints to the app
    from . import auth
    from . import pages
    from . import check
    from . import config

    app.register_blueprint(auth.bp)
    app.register_blueprint(pages.bp)
    app.register_blueprint(check.bp)
    app.register_blueprint(config.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
