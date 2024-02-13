create-venv:
	python3 -m venv ./venv

activate-venv:
	source ./venv/bin/activate

install-dependencies: ../requirements.txt
	pip install	 -r ../requirements.txt

fmt:
	ruff --fix .

db-migrations:
	python manage.py migrate

tests:
	python manage.py test

dev-server:
	python manage.py runserver 7070

lint:
	ruff . && mypy .

check-before-deploy:
	python manage.py check --deploy