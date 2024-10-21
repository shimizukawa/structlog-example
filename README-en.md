# structlog-example
This is a demo app that shows how to integrate structlog with Django, Celery, and Sentry.

- Set the structlog formatter for the standard logging library.
- Logs created using the standard logging library are formatted with the structlog formatter.
- Logs created through structlog are formatted using the structlog formatter set in the standard logging.

refs:
- [Rendering Using structlog-based Formatters Within logging](https://www.structlog.org/en/latest/standard-library.html#rendering-using-structlog-based-formatters-within-logging)

## Dependencies

- structlog
- django
- celery[redis]
- django-structlog[celery]
- structlog-sentry
- sentry-sdk

## Setup

```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
$ . $HOME/.cargo/env
$ uv sync
```

## Run demo

```
$ docker compose up -d
$ source .venv/bin/activate
(structlog-example) $ cd djapp
(structlog-example) $ python manage.py migrate
(structlog-example) $ python manage.py createsuperuser --username admin --email admin@example.com
Password: <ENTER YOUR PASSWORD>
(structlog-example) $ python manage.py runserver
```

Once the application is running, you can access it at http://127.0.0.1:8000/admin/ and log in using the `admin` credentials.

## Logging with stdlib and structlog

```
2024-09-23T06:01:31.675294Z [debug    ] (0.000) SELECT ... [django.db.backends] filename=utils.py func_name=debug_sql lineno=151
2024-09-23T06:01:31.678409Z [debug    ] こんにちは structlog!               [djapp.log] filename=log.py func_name=dict_config lineno=74
```

## Integrating django-structlog

By adding `django_structlog....` to `INSTALLED_APPS` and `MIDDLEWARE`, the logging will change as follows:

- Output logs when a request starts and ends.
- Logs during request processing will include context information like request_id and user_id.

```
2024-09-23T06:02:16.182528Z [info     ] request_started                [django_structlog.middlewares.request] filename=request.py func_name=prepare ip=127.0.0.1 lineno=161 request=GET /admin/ request_id=af3a4bb6-9ccd-4caa-aa66-0a470325cc99 user_agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 user_id=1
2024-09-23T06:02:16.212422Z [debug    ] (0.000) SELECT ...; [django.db.backends] filename=utils.py func_name=debug_sql ip=127.0.0.1 lineno=151 request_id=af3a4bb6-9ccd-4caa-aa66-0a470325cc99 user_id=1
2024-09-23T06:02:16.212872Z [info     ] request_finished               [django_structlog.middlewares.request] code=200 filename=request.py func_name=handle_response ip=127.0.0.1 lineno=109 request=GET /admin/ request_id=af3a4bb6-9ccd-4caa-aa66-0a470325cc99 user_id=1
```

## Adding Celery and Integrating django-structlog[celery]

The structlog renderer is also applied to the debug logs of Celery. However, if the messages contain line breaks (around `chain`), they are output as is. This is due to the output from the console renderer designed for human readability.

```
2024-09-23T07:05:37.100553Z [info     ] request_started                [django_structlog.middlewares.request] filename=request.py func_name=prepare ip=127.0.0.1 lineno=161 request=POST /admin/app1/value/6/change/ request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 user_id=1
2024-09-23T07:05:37.101132Z [debug    ] (0.000) BEGIN; args=None; alias=default [django.db.backends] filename=utils.py func_name=debug_sql ip=127.0.0.1 lineno=151 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.101608Z [debug    ] (0.000) SELECT "app1_value"."id", "app1_value"."x", "app1_value"."y", "app1_value"."result" FROM "app1_value" WHERE "app1_value"."id" = 6 LIMIT 21; args=(6,); alias=default [django.db.backends] filename=utils.py func_name=debug_sql ip=127.0.0.1 lineno=151 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.103037Z [debug    ] (0.000) UPDATE "app1_value" SET "x" = 2, "y" = 6, "result" = 7 WHERE "app1_value"."id" = 6; args=(2, 6, 7, 6); alias=default [django.db.backends] filename=utils.py func_name=debug_sql ip=127.0.0.1 lineno=151 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.107277Z [debug    ] 
def chain(*args, **kwargs):
    return 1
 [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.108418Z [debug    ] 
def xstarmap(task, it):
    return 1
 [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.108836Z [debug    ] 
def accumulate(self, *args, **kwargs):
    return 1
 [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.109300Z [debug    ] 
def chord(self, header, body, partial_args=0, interval=1, countdown=2, max_retries=3, eager=4, **kwargs):
    return 1
 [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.109714Z [debug    ] 
def chunks(task, it, n):
    return 1
 [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.110117Z [debug    ] 
def calc(pk):
    return 1
   [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.110589Z [debug    ] 
def unlock_chord(self, group_id, callback, interval=0, max_retries=1, result=2, Result=3, GroupResult=4, result_from_tuple=5, **kwargs):
    return 1
 [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.111056Z [debug    ] 
def group(self, tasks, result, group_id, partial_args, add_to_parent=0):
    return 1
 [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.111452Z [debug    ] 
def xmap(task, it):
    return 1
 [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.111819Z [debug    ] 
def backend_cleanup():
    return 1
 [celery.utils.functional] filename=functional.py func_name=head_from_fun ip=127.0.0.1 lineno=335 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.150297Z [debug    ] (0.000) SELECT "app1_value"."id", "app1_value"."x", "app1_value"."y", "app1_value"."result" FROM "app1_value" WHERE "app1_value"."id" = 6 LIMIT 21; args=(6,); alias=default [django.db.backends] filename=utils.py func_name=debug_sql ip=127.0.0.1 lineno=151 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.150508Z [info     ] add                            [app1.tasks] filename=tasks.py func_name=calc ip=127.0.0.1 lineno=17 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1 x=2 y=6
2024-09-23T07:05:37.151072Z [debug    ] (0.000) UPDATE "app1_value" SET "x" = 2, "y" = 6, "result" = 8 WHERE "app1_value"."id" = 6; args=(2, 6, 8, 6); alias=default [django.db.backends] filename=utils.py func_name=debug_sql ip=127.0.0.1 lineno=151 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.151726Z [debug    ] (0.000) SELECT "app1_value"."id", "app1_value"."x", "app1_value"."y", "app1_value"."result" FROM "app1_value" WHERE "app1_value"."id" = 6 LIMIT 21; args=(6,); alias=default [django.db.backends] filename=utils.py func_name=debug_sql ip=127.0.0.1 lineno=151 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.151907Z [info     ] add                            [app1.tasks] filename=tasks.py func_name=calc ip=127.0.0.1 lineno=17 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1 x=2 y=6
2024-09-23T07:05:37.156035Z [info     ] Task app1.tasks.calc[d84a985b-c789-43df-8ff9-46c84681bc01] succeeded in 0.004551626000022679s: 8 [celery.app.trace] filename=trace.py func_name=info ip=127.0.0.1 lineno=128 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.156247Z [info     ] Task app1.tasks.calc[d60abef8-31bc-4eb8-bdb0-c17903cc8340] succeeded in 0.006245978999970703s: 8 [celery.app.trace] filename=trace.py func_name=info ip=127.0.0.1 lineno=128 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.157303Z [debug    ] (0.000) INSERT INTO "django_admin_log" ("action_time", "user_id", "content_type_id", "object_id", "object_repr", "action_flag", "change_message") VALUES ('2024-09-23 07:05:37.156611', 1, 7, '6', 'x=2, y=6, result=7', 2, '[{"changed": {"fields": ["Y"]}}]'); args=['2024-09-23 07:05:37.156611', 1, 7, '6', 'x=2, y=6, result=7', 2, '[{"changed": {"fields": ["Y"]}}]']; alias=default [django.db.backends] filename=utils.py func_name=debug_sql ip=127.0.0.1 lineno=151 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.195652Z [debug    ] (0.038) COMMIT; args=None; alias=default [django.db.backends] filename=utils.py func_name=debug_transaction ip=127.0.0.1 lineno=181 request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
2024-09-23T07:05:37.195967Z [info     ] request_finished               [django_structlog.middlewares.request] code=302 filename=request.py func_name=handle_response ip=127.0.0.1 lineno=109 request=POST /admin/app1/value/6/change/ request_id=1725afad-b78d-4037-bfa9-a9bd63b9a4af user_id=1
[23/Sep/2024 07:05:37] "POST /admin/app1/value/6/change/ HTTP/1.1" 302 0
```

When the same operation logs are output in JSON output, it looks like the following.
The renderer switch is handled in `djapp/log.py`.

Even if the messages contain line breaks (around `chain`), you can see that they are properly stored within the JSON format.

```
{"event": "(0.000) SELECT \"django_session\".\"session_key\", \"django_session\".\"session_data\", \"django_session\".\"expire_date\" FROM \"django_session\" WHERE (\"django_session\".\"expire_date\" > '2024-09-23 07:12:41.242868' AND \"django_session\".\"session_key\" = 'h3r177ov3g2evdwehgdxwgmghsy7oxbp') LIMIT 21; args=('2024-09-23 07:12:41.242868', 'h3r177ov3g2evdwehgdxwgmghsy7oxbp'); alias=default", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "level": "debug", "logger": "django.db.backends", "timestamp": "2024-09-23T07:12:41.243997Z", "filename": "utils.py", "lineno": 151, "func_name": "debug_sql"}
{"event": "(0.000) SELECT \"auth_user\".\"id\", \"auth_user\".\"password\", \"auth_user\".\"last_login\", \"auth_user\".\"is_superuser\", \"auth_user\".\"username\", \"auth_user\".\"first_name\", \"auth_user\".\"last_name\", \"auth_user\".\"email\", \"auth_user\".\"is_staff\", \"auth_user\".\"is_active\", \"auth_user\".\"date_joined\" FROM \"auth_user\" WHERE \"auth_user\".\"id\" = 1 LIMIT 21; args=(1,); alias=default", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "level": "debug", "logger": "django.db.backends", "timestamp": "2024-09-23T07:12:41.244904Z", "filename": "utils.py", "lineno": 151, "func_name": "debug_sql"}
{"request": "POST /admin/app1/value/6/change/", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36", "event": "request_started", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "info", "logger": "django_structlog.middlewares.request", "timestamp": "2024-09-23T07:12:41.245253Z", "filename": "request.py", "lineno": 161, "func_name": "prepare"}
{"event": "(0.000) BEGIN; args=None; alias=default", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "django.db.backends", "timestamp": "2024-09-23T07:12:41.245824Z", "filename": "utils.py", "lineno": 151, "func_name": "debug_sql"}
{"event": "(0.000) SELECT \"app1_value\".\"id\", \"app1_value\".\"x\", \"app1_value\".\"y\", \"app1_value\".\"result\" FROM \"app1_value\" WHERE \"app1_value\".\"id\" = 6 LIMIT 21; args=(6,); alias=default", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "django.db.backends", "timestamp": "2024-09-23T07:12:41.246323Z", "filename": "utils.py", "lineno": 151, "func_name": "debug_sql"}
{"event": "(0.000) UPDATE \"app1_value\" SET \"x\" = 1, \"y\" = 7, \"result\" = 8 WHERE \"app1_value\".\"id\" = 6; args=(1, 7, 8, 6); alias=default", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "django.db.backends", "timestamp": "2024-09-23T07:12:41.247753Z", "filename": "utils.py", "lineno": 151, "func_name": "debug_sql"}
{"event": "\ndef chain(*args, **kwargs):\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.252393Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "\ndef xstarmap(task, it):\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.253565Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "\ndef accumulate(self, *args, **kwargs):\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.253985Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "\ndef chord(self, header, body, partial_args=0, interval=1, countdown=2, max_retries=3, eager=4, **kwargs):\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.254410Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "\ndef chunks(task, it, n):\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.254826Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "\ndef calc(pk):\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.255209Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "\ndef unlock_chord(self, group_id, callback, interval=0, max_retries=1, result=2, Result=3, GroupResult=4, result_from_tuple=5, **kwargs):\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.255672Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "\ndef group(self, tasks, result, group_id, partial_args, add_to_parent=0):\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.256118Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "\ndef xmap(task, it):\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.256490Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "\ndef backend_cleanup():\n    return 1\n", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "celery.utils.functional", "timestamp": "2024-09-23T07:12:41.256838Z", "filename": "functional.py", "lineno": 335, "func_name": "head_from_fun"}
{"event": "(0.000) SELECT \"app1_value\".\"id\", \"app1_value\".\"x\", \"app1_value\".\"y\", \"app1_value\".\"result\" FROM \"app1_value\" WHERE \"app1_value\".\"id\" = 6 LIMIT 21; args=(6,); alias=default", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "django.db.backends", "timestamp": "2024-09-23T07:12:41.295730Z", "filename": "utils.py", "lineno": 151, "func_name": "debug_sql"}
{"x": 1, "y": 7, "event": "add", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "info", "logger": "app1.tasks", "timestamp": "2024-09-23T07:12:41.295977Z", "filename": "tasks.py", "lineno": 17, "func_name": "calc"}
{"event": "Task app1.tasks.calc[ca1c1a67-5e03-4807-93e3-1e5260c46478] succeeded in 0.004687687000000551s: 8", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "info", "logger": "celery.app.trace", "timestamp": "2024-09-23T07:12:41.300048Z", "filename": "trace.py", "lineno": 128, "func_name": "info"}
{"event": "(0.000) INSERT INTO \"django_admin_log\" (\"action_time\", \"user_id\", \"content_type_id\", \"object_id\", \"object_repr\", \"action_flag\", \"change_message\") VALUES ('2024-09-23 07:12:41.300351', 1, 7, '6', 'x=1, y=7, result=8', 2, '[{\"changed\": {\"fields\": [\"X\"]}}]'); args=['2024-09-23 07:12:41.300351', 1, 7, '6', 'x=1, y=7, result=8', 2, '[{\"changed\": {\"fields\": [\"X\"]}}]']; alias=default", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "django.db.backends", "timestamp": "2024-09-23T07:12:41.300937Z", "filename": "utils.py", "lineno": 151, "func_name": "debug_sql"}
{"event": "(0.027) COMMIT; args=None; alias=default", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "debug", "logger": "django.db.backends", "timestamp": "2024-09-23T07:12:41.328429Z", "filename": "utils.py", "lineno": 181, "func_name": "debug_transaction"}
{"code": 302, "request": "POST /admin/app1/value/6/change/", "event": "request_finished", "ip": "127.0.0.1", "request_id": "36755c1f-84cb-43c1-b75f-88b4acd7e75e", "user_id": 1, "level": "info", "logger": "django_structlog.middlewares.request", "timestamp": "2024-09-23T07:12:41.328682Z", "filename": "request.py", "lineno": 109, "func_name": "handle_response"}
[23/Sep/2024 07:12:41] "POST /admin/app1/value/6/change/ HTTP/1.1" 302 0
```
