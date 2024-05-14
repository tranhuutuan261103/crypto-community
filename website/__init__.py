import os

from flask import Flask
from flask_cors import CORS
from flask_uploads import configure_uploads, UploadSet, IMAGES

# Khởi tạo Flask-Uploads
photos = UploadSet('photos', IMAGES)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['UPLOADED_PHOTOS_DEST'] = 'photos'
    configure_uploads(app, photos)

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
    from .controller.auth import bp as auth_bp
    from .controller.posts import bp as posts_bp
    from .controller.comments import bp as comments_bp
    from .controller.articles import bp as articles_bp
    from .controller.admin import bp as admin_bp
    CORS(posts_bp)

    app.register_blueprint(hello, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(posts_bp, url_prefix='/post')
    app.register_blueprint(comments_bp, url_prefix='/comments')
    app.register_blueprint(articles_bp, url_prefix='/articles')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    return app