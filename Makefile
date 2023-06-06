ENV=.venv
PYTHON=$(ENV)/bin/python3
PYTHON_VERSION=3.8
FLASK_APP=app
FLASK := FLASK_APP=$(FLASK_APP) $(ENV)/bin/flask

run: $(ENV)/bin/activate
	$(FLASK) run

debug: $(ENV)/bin/activate
	FLASK_DEBUG=True $(FLASK) run

clean:
	rm -rf __pycache__
	rm -rf $(ENV)

$(ENV)/bin/activate: requirements.txt
	python3 -m venv $(ENV)
	$(ENV)/bin/pip install -r requirements.txt

