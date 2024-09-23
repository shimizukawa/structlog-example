# structlog-example
structlog を Django, Celery, Sentry で連携するデモアプリです。

- 標準ライブラリのlogging経由でのログ出力は、structlogでフォーマットします。
- structlog経由でのログ出力は、標準のloggingのフォーマッターを経由してstructlogでフォーマットします。

refs:
- [Rendering Using structlog-based Formatters Within logging](https://www.structlog.org/en/latest/standard-library.html#rendering-using-structlog-based-formatters-within-logging)

## 依存ライブラリ

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

## デモの実行

```
$ source .venv/bin/activate
(structlog-example) $ cd djapp
(structlog-example) $ python manage.py migrate
(structlog-example) $ python manage.py createsuperuser --username admin --email admin@example.com
Password: <ENTER YOUR PASSWORD>
(structlog-example) $ python manage.py runserver
```

起動したら、 http://127.0.0.1:8000/admin/ にアクセスして `admin` でログインできます。
