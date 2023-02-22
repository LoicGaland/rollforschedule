ENV=.env

run: $(ENV)/bin/activate
	$(ENV)/bin/python3 app.py

clean:
	rm -rf __pycache__
	rm -rf $(ENV)

$(ENV)/bin/activate: requirements.txt
	python3 -m venv $(ENV)
	$(ENV)/bin/pip install -r requirements.txt

