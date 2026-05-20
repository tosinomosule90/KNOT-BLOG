from flask import Flask
from .extension import db
import secrets
from .view import company



def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    # Configure FIRST
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    from .extension import login_manager

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(company)

    return app