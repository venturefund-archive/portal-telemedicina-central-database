# Install local dependencies
pip install --upgrade pip
pip install -r central_database/requirements/local.txt

# Install pre-commit hooks: https://pre-commit.com/. Amongst them is the auto-update of dependencies.
pre-commit install -c central_database/.pre-commit-config.yaml
