.PHONY: lint test

lint:
	python -m pylint check_monit.py

test:
	python -m unittest -v test_check_monit.py
coverage:
	python -m coverage run -m unittest -b test_check_monit.py
	python -m coverage report -m --include check_monit.py
