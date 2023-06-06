from app import db, Table, Player, app

with app.app_context():
    db.drop_all()
    db.create_all()
