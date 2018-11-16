#!/bin/bash

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

docker-compose down -v

docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py loaddata user_type.json

docker-compose up
