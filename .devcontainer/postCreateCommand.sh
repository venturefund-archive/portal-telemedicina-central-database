# Install local dependencies
pip install --upgrade pip
pip install -r central_database/requirements/local.txt

# Install pre-commit hooks: https://pre-commit.com/. Amongst them is the auto-update of dependencies.
pre-commit install -c central_database/.pre-commit-config.yaml

# Configure the local postgres database
python central_database/manage.py migrate
python central_database/manage.py createsuperuser --username=admin --email=admin@admin.com
