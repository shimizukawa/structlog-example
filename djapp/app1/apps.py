from django.apps import AppConfig
from django.db.models import signals


class App1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app1"

    def ready(self):
        from .models import Value
        from . import tasks

        def add(sender, instance: Value, **kwargs):
            tasks.calc.delay(instance.pk)

        signals.post_save.connect(add, sender=Value)
