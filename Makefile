ENV=.venv
PYTHON=$(ENV)/bin/python3
PYTHON_VERSION=3.8
FLASK_APP=rollforschedule/app:app
FLASK := FLASK_APP=$(FLASK_APP) $(ENV)/bin/flask

run: migrate
	gunicorn --chdir ./rollforschedule app:app

debug: migrate
	python3 -m venv $(ENV)
	$(ENV)/bin/pip install -r requirements.txt
	FLASK_DEBUG=True $(FLASK) run

clean:
	rm -rf __pycache__
	rm -rf $(ENV)

migrate: $(ENV)/bin/activate
	$(PYTHON) rollforschedule/init_db.py

$(ENV)/bin/activate: requirements.txt
	python3 -m venv $(ENV)
	$(ENV)/bin/pip install -r requirements.txt

build:
	pip install -r requirements.txt
	python rollforschedule/init_db.py
