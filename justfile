# setup
setup:
    python -m venv venv
    ./venv/bin/pip install -r requirements.txt

# install deps
install:
    pip install -r requirements.txt

# run the pipeline
run:
    python -m animal_etl.pipeline

# run tests
test:
    pytest -v

# lint code
lint:
    pre-commit run --all-files
