from django.db import models


class TimeStampedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        abstract = True