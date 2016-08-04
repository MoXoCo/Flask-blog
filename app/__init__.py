from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app():
    db_path = 'db1.sqlite'

    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.secret_key = 'TODO fixme'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)

    db.init_app(app)
    db.app = app

    from .auth import auth
    from .main import main
    from .api import api


    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')


    return app