# Install local dependencies
pip install --upgrade pip
pip install -r central_database/requirements/local.txt

# Install pre-commit hooks: https://pre-commit.com/. Amongst them is the auto-update of dependencies.
pre-commit install -c central_database/.pre-commit-config.yaml

# Configure the local postgres database
echo Applying migrations...
python central_database/manage.py migrate
echo Creating superuser...
cat <<EOF | python central_database/manage.py shell
from django.contrib.auth import get_user_model
from os import environ

USR=environ['DJANGO_SUPERUSER_USERNAME']
EMAIL=environ['DJANGO_SUPERUSER_EMAIL']
PSWD=environ['DJANGO_SUPERUSER_PASSWORD']

User = get_user_model()  # Get the currently active user model,

if not User.objects.filter(username=USR).exists():
    User.objects.create_superuser(USR, EMAIL, PSWD)
else:
    print(f'User "{USR}" already exists, not created')
EOF
