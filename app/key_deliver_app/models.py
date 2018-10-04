from django.db import models
from django.core.validators import RegexValidator


class KeyManager(models.Manager):
    def count_delivered(self):
        return super().get_queryset().filter(is_delivered=True).count()

    def count_repayed(self):
        return super().get_queryset().filter(is_repayed=True).count()


class Key(models.Model):
    value = models.CharField(
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(regex='^.{4}$', message='Length must be 4')
        ]
    )
    is_delivered = models.BooleanField(default=False)
    is_repayed = models.BooleanField(default=False)

    objects = KeyManager()
