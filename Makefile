ENV=.env
PYTHON=$(ENV)/bin/python3
PYTHON_VERSION=3.8

run: $(ENV)/bin/activate
	$(PYTHON) app.py

build: $(ENV)/bin/activate
	$(PYTHON) build.py

clean:
	rm -rf __pycache__
	rm -rf $(ENV)
	rm -rf build

$(ENV)/bin/activate: requirements.txt
	python3 -m venv $(ENV)
	$(ENV)/bin/pip install -r requirements.txt

