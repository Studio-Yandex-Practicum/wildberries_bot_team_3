#!/bin/bash

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - executing command"

poetry run python expert_system/manage.py migrate
poetry run python expert_system/manage.py createsuperuser --noinput
poetry run python expert_system/manage.py runserver

exec "$@"
