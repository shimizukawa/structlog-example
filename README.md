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

## stdlibとstructlogによるログ出力

```
2024-09-23T06:01:31.675294Z [debug    ] (0.000) SELECT ... [django.db.backends] filename=utils.py func_name=debug_sql lineno=151
2024-09-23T06:01:31.678409Z [debug    ] こんにちは structlog!               [djapp.log] filename=log.py func_name=dict_config lineno=74
```

## django-structlog の組み込み

`INSTALLED_APPS` と `MIDDLEWARE` へ `django_structlog....` を追加すると、以下のようにログが変化します。

- リクエスト開始時、終了時のログ出力
- リクエスト処理中のログ出力に、コンテキスト情報 `request_id`, `user_id` の追加

```
2024-09-23T06:02:16.182528Z [info     ] request_started                [django_structlog.middlewares.request] filename=request.py func_name=prepare ip=127.0.0.1 lineno=161 request=GET /admin/ request_id=af3a4bb6-9ccd-4caa-aa66-0a470325cc99 user_agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 user_id=1
2024-09-23T06:02:16.212422Z [debug    ] (0.000) SELECT ...; [django.db.backends] filename=utils.py func_name=debug_sql ip=127.0.0.1 lineno=151 request_id=af3a4bb6-9ccd-4caa-aa66-0a470325cc99 user_id=1
2024-09-23T06:02:16.212872Z [info     ] request_finished               [django_structlog.middlewares.request] code=200 filename=request.py func_name=handle_response ip=127.0.0.1 lineno=109 request=GET /admin/ request_id=af3a4bb6-9ccd-4caa-aa66-0a470325cc99 user_id=1
```
