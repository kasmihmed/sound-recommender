install-dependencies: requirements.txt
	pip install	 -r ./requirements.txt

lint: install-dependencies
	ruff .

fmt: install-dependencies
	ruff --fix .

tests: install-dependencies
	cd soundrecommender && python manage.py test