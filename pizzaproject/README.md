## Project setup
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate

## Create user for django
docker-compose run web python manage.py createsuperuser

## Run test 
docker-compose run web python manage.py test pizza; To run test app pizza

## Run service
docker-compose up