import os

from werkzeug.security import generate_password_hash

from app import db, app
from models import Player

# Run to initialize or reset SQLite DB with a single admin user. The script
# uses environment variables to define the username adress and password.


def get_var(var_name):
    # Check if a var exists and returns it. If it doesn't, check if there's a
    # another var with a path to the the var. This behaviour is meant to handle
    # Docker secrets.

    var = os.environ.get(var_name)
    if var:
        return var

    var_path = os.environ.get(var_name + "_PATH")
    if not var_path:
        raise Exception(f"No env var found for {var_name} or {var_name}_PATH")

    with open(var_path) as f:
        var = f.read()

    return var


if __name__ == "__main__":

    admin_email = get_var("ADMIN_EMAIL")
    admin_password = get_var("ADMIN_PASSWORD")

    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = Player(
            username="admin",
            email=admin_email,
            password=generate_password_hash(admin_password, method='scrypt'),
            admin_rights=True
        )
        db.session.add(admin)
        db.session.commit()
