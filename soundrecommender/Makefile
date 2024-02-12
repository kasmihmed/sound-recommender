
install-dependencies: ../requirements.txt
	pip install	 -r ../requirements.txt

fmt:
	ruff --fix .

tests:
	python manage.py test

lint:
	ruff . && mypy .

check-before-deploy:
	python manage.py check --deploy