# setup
setup:
    python3 -m venv .venv
    ./.venv/bin/pip install -r requirements.txt

# install deps
install:
    ./.venv/bin/pip install -r requirements.txt

# run the pipeline
run:
    ./.venv/bin/python -m animal_etl.pipeline

# run tests
test:
    ./.venv/bin/pytest -v

# lint code
lint:
    ./.venv/bin/pre-commit run --all-files
