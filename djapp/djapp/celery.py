import copy
import logging
import os

import celery
import celery.signals
from django.conf import settings
from django.utils.module_loading import import_string
from django_structlog.celery.steps import DjangoStructLogInitStep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djapp.settings")

app = celery.Celery("djapp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# initialize django-structlog
app.steps["worker"].add(DjangoStructLogInitStep)

@celery.signals.setup_logging.connect
def setup_logging(*, loglevel=logging.INFO, **kwargs):
    """celeryのlogging設定をオーバーライドし、起動時のloglevelのみ適用する

    refs:
    - https://django-structlog.readthedocs.io/en/latest/celery.html
    - https://docs.celeryq.dev/en/stable/userguide/signals.html#setup-logging
    """
    logging_setting = copy.deepcopy(settings.LOGGING)
    logging_setting["loggers"][""]["level"] = loglevel
    configure = import_string(settings.LOGGING_CONFIG)
    configure(logging_setting)
