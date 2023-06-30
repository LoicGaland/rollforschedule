ENV=.venv
PYTHON=$(ENV)/bin/python3
PYTHON_VERSION=3.8
FLASK_APP=app:app
FLASK := FLASK_APP=$(FLASK_APP) $(ENV)/bin/flask

run: build
	$(FLASK) run

debug: build
	$(PYTHON) init_db.py
	FLASK_DEBUG=True $(FLASK) run

build: $(ENV)/bin/activate
	$(PYTHON) init_db.py

clean:
	rm -rf __pycache__
	rm -rf $(ENV)

$(ENV)/bin/activate: requirements.txt
	python3 -m venv $(ENV)
	$(ENV)/bin/pip install -r requirements.txt
