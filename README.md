# Django Movie Theater

## Pusher
create a new pusher app and update settings.py accordingly:
```
PUSHER_APP_ID = ""
PUSHER_KEY = ""
PUSHER_SECRET = ""
PUSHER_CLUSTER = ""
```

## Facebook
create a facebook app and update seettings.py accordingly:
```
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
```

## Dev Environment
Run the server with:
```
docker-compose up -d db
docker-compose up -d web
```

Run the migrations:

```
docker-compose exec web python manage.py migrate
```

Provision the database:
```
docker-compose exec db /usr/lib/postgresql/9.6/bin/psql -Upostgres -f /code/storage/provisions/repertoires.sql
docker-compose exec db /usr/lib/postgresql/9.6/bin/psql -Upostgres -f /code/storage/provisions/rooms.sql
```

Create superuser for admin panel:

```
docker-compose exec web python manage.py createsuperuser
```


start the worker

```
docker-compose exec web
export C_FORCE_ROOT='true'
python manage.py celeryd --beat
```

Navigate to:

 1. http://localhost:8000/
 1. http://localhost:8000/admin


## Libraries used
env

1. docker
1. docker postgres
1. docker python 2.7

python

1. Django
1. psycopg2
1. social-auth-app-django
1. pusher
1. django-celery
1. django-request

frontend

1. bootstrap
1. jquery

uses third party

1. facebook
1. pusher