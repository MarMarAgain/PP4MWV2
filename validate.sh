#!/bin/bash

PROJECT_DIR="PP4MWV2"
APP_DIRS="accounts" "purchase" "workshops" "other_pages"

echo "Running Django checks..."
python manage.py check

echo "Running flake8..."
flake8 .

echo "Running pylint..."
pylint $PROJECT_DIR/ $APP_DIRS

echo "Running bandit..."
bandit -r $PROJECT_DIR/ $APP_DIRS

echo "Running safety..."
safety check

echo "Checking for outdated dependencies..."
pip-check

echo "Validating migrations..."
python manage.py makemigrations --check

echo "Running tests..."
python manage.py test

echo "All checks completed."
