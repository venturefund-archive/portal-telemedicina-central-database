# Install local dependencies
pip install --upgrade pip
pip install poetry==1.1.14
poetry config virtualenvs.create false
poetry install

# Install pre-commit hooks: https://pre-commit.com/. Amongst them is the auto-update of dependencies.
pre-commit install -c central_database/.pre-commit-config.yaml

# Configure the local postgres database
echo Cleaning database...
python central_database/manage.py flush --noinput
echo Applying migrations...
python central_database/manage.py migrate
echo Creating superuser...
python central_database/manage.py createsuperuser --noinput  # Usr: admin Pwd: admin
