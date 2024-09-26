from django.db import models


class Value(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    result = models.IntegerField(null=True, default=None)

    def __str__(self):
        return f"x={self.x}, y={self.y}, result={self.result}"
