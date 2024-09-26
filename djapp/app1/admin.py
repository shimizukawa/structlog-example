from django.contrib import admin

from .models import Value


@admin.register(Value)
class Admin(admin.ModelAdmin):
    readonly_fields = ("result",)
    list_display = ("pk", "x", "y", "result")
