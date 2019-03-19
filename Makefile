CODE = tic_tac_toe
BIN = .venv/bin/

init:
	python3 -m venv .venv
	$(BIN)pip install -r requirements.txt

test:
	$(BIN)python -m pytest -vv --cov=$(CODE) $(args)

lint:
	$(BIN)flake8 --jobs 4 --statistics $(CODE) tests
	$(BIN)pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(BIN)black --py36 --line-length=100 --check $(CODE) tests

pretty:
	$(BIN)isort --apply --recursive $(CODE) tests
	$(BIN)black --py36 --line-length=100 $(CODE) tests

precommit_install:
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

start_server:
	PYTHONPATH='.' python tic_tac_toe/server.py 'localhost' 9090 3x3

start_client:
	PYTHONPATH='.' python tic_tac_toe/client.py 'localhost' 9090
