# Project Management API Documentation


For documentation: http://localhost:8000/api/schema/swagger-ui/
and http://localhost:8000/api/schema/redoc/

this project can be used in production changing the dev.sh to production.sh which uses Gunicorn and in setting Debug needs to be false

## Docker Setup

Install Docker Desktop(on the docker desktop application) and run the following command to start the application: Use a linux Distro preferably Ubuntu

```sh
docker-compose up --build
```

Or in detached mode( use this -f docker-compose.yml file name)

```sh
docker compose up -d
```

If not using Docker, use Python 3.13 and configure PostgreSQL correctly:

```add it to .env
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

include postgres data in .env

do 
pipenv install

python manage.py migrate

python manage.py runserver


