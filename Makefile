ENV=.env
PYTHON=$(ENV)/bin/python3
PYTHON_VERSION=3.8

run: $(ENV)/bin/activate
	$(PYTHON) app.py

dev: $(ENV)/bin/activate
	FLASK_DEBUG=development flask run

clean:
	rm -rf __pycache__
	rm -rf $(ENV)

$(ENV)/bin/activate: requirements.txt
	python3 -m venv $(ENV)
	$(ENV)/bin/pip install -r requirements.txt

