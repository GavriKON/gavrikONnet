from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager
from main.config import Config
from flask_migrate import Migrate
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    from main.users.routes import users
    from main.posts.routes import posts
    from main.home.routes import main
    from main.errors.handlers import errors
    from main.cli import bp
    app.register_blueprint(users)

    app.register_blueprint(posts)

    
    app.register_blueprint(main)

    app.register_blueprint(errors)

    app.register_blueprint(bp)
    return app


