from django.db import models
from django.core.validators import RegexValidator


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
