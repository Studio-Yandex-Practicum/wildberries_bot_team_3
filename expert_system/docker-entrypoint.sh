until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - executing command"

poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py createsuperuser --noinput
poetry run python manage.py runserver

exec "$@"
