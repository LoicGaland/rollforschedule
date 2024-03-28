import os

from werkzeug.security import generate_password_hash

from app import db, app
from models import Player

with app.app_context():
    db.drop_all()
    db.create_all()
    admin = Player(
        username="admin",
        email=os.environ["ADMIN_EMAIL"],
        password=generate_password_hash(os.environ["ADMIN_PASSWORD"], method='scrypt'),
        admin_rights=True
    )
    db.session.add(admin)
    db.session.commit()
