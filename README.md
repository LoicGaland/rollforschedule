# Roll For Schedule

## Description
This app is meant to help our group manage our everlasting scheduling conflicts for our TTRPG sessions.

## Dependencies
- Python 3.10
- Flask
- Flask Admin
- Flask Login
- Flask SQLAlchemy
- Werkzeug
- Gunicorn

## Quickstart

Set environment variables for admin username and password
```
export ADMIN_EMAIL=[admin_email]
export ADMIN_PASSWORD=[admin_password]
```

Then run with either a Python virtual environment or Docker

### Python virtual environment
```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python3 rollforschedule/init_db.py
gunicorn --chdir ./rollforschedule app:app
```

### Docker
```
docker compose up
```

