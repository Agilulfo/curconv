.PHONY:
	cheeshop \
	isort \
	flake8 \
	test \

cheeseshop:
	pip install -r requirements.txt

isort:
	isort

flake8:
	flake8 .

test:
	nosetests --ipdb
