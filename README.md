# structlog-example
structlog with Django, Celery, Sentry


## dependencies

- structlog
- django
- celery
- django-structlog[celery]
- structlog-sentry
- sentry-sdk

## Setup

```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
$ . $HOME/.cargo/env
$ uv sync
```

## Run django

```
$ source .venv/bin/activate
(structlog-example) $ cd djapp
(structlog-example) $ python manage.py migrate
(structlog-example) $ python manage.py createsuperuser --username admin --email admin@example.com
Password: <ENTER YOUR PASSWORD>
(structlog-example) $ python manage.py runserver
```

Then open http://127.0.0.1:8000/admin/ and login by `admin` with your password.
