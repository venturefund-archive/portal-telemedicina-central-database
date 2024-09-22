# Makefile for Central Database project

# Variables
DC := docker-compose
BACKEND := $(DC) run backend
FRONTEND := $(DC) run frontend

# Backend commands
backend-migrations:
	$(BACKEND) python manage.py makemigrations

backend-migrate:
	$(BACKEND) python manage.py migrate

backend-loaddata:
	$(BACKEND) sh -c "find /app/vaccines/fixtures -name '*.json' | xargs python manage.py loaddata"

backend-createsuperuser:
	$(BACKEND)  python manage.py createsuperuser --noinput

backend-start:
	$(DC) up backend

backend-build:
	$(DC) build backend

backend-stop:
	$(DC) down backend

backend-test:
	$(BACKEND) python manage.py test

backend-restart:
	$(DC) restart backend

# Frontend commands
frontend-start:
	$(DC) up frontend

# Database commands
db-start:
	$(DC) up postgres

# Documentation commands
docs-backend:
	cd docs && sphinx-autobuild . _build/html --host 0.0.0.0 --port 8001

docs-frontend:
	cd docs/frontend && vuepress dev --port 8002

docs-all:
	$(DC) up docs-backend docs-frontend

# Combined commands
setup: backend-migrate backend-loaddata backend-createsuperuser

start-all:
	$(DC) up

stop-all:
	$(DC) down

# Development workflow
dev: setup start-all

# Cleanup
clean:
	$(DC) down -v
	$(DC) rm -f

.PHONY: backend-migrate backend-loaddata backend-createsuperuser backend-start backend-test \
        frontend-start db-start docs-backend docs-frontend docs-all \
        setup start-all stop-all dev clean