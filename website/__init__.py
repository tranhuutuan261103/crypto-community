import os

from flask import Flask
from .db_config.firebase import default_app

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .controller.hello import hello
    from .controller.auth import auth
    from .controller.post import post

    app.register_blueprint(hello, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(post, url_prefix='/post')

    return app