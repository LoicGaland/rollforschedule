from app import db, create_app
from models import Table, Player

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
