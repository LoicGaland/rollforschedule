import os

from admin import TableView, PlayerView, AvailabilityView, AdminView
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    from scheduler import scheduler as scheduler_blueprint

    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import Player, Table, Availability

    @login_manager.user_loader
    def load_user(user_id):
        return Player.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(scheduler_blueprint)

    app.config['FLASK_ADMIN_SWATCH'] = 'slate'
    admin = Admin(
        app,
        'Roll for Schedule',
        url='/',
        index_view=AdminView(name='RFSAdmin'),
        template_mode='bootstrap3'
    )

    admin.add_view(PlayerView(Player, db.session))
    admin.add_view(TableView(Table, db.session))
    admin.add_view(AvailabilityView(Availability, db.session))

    return app


app = create_app()
