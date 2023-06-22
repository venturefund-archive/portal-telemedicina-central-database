git config --global --add safe.directory /workspace

# Install local dependencies
pip install --upgrade pip
pip install pre-commit==2.19.0
pip install flake8==3.9.2


# Install pre-commit hooks: https://pre-commit.com/. Amongst them is the auto-update of dependencies.
pre-commit install -c central_database/.pre-commit-config.yaml
