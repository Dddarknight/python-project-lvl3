make lint: #запуск flake8
	poetry run flake8 page_loader

install:
	poetry install

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

build:
	poetry build

publish:
	poetry publish --dry-run

test:
	poetry run pytest

package-install:
	python3 -m pip install dist/hexlet_code-0.1.0-py3-none-any.whl