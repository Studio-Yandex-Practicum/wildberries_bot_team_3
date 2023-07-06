#!/bin/bash

poetry run python expert_system/manage.py makemigrations
poetry run python expert_system/manage.py migrate
poetry run python expert_system/manage.py createsuperuser --noinput
poetry run python expert_system/manage.py runserver

exec "$@"
