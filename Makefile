lint:
	ruff check .
	mypy .

test:
	pytest .

	python examples/simple/main.py
	python examples/wrap/main.py

all: lint test
