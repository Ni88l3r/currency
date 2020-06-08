from django.db import models
from django.utils import timezone

from rate import model_choices as mch
from rate.utils import to_decimal

time_zone = timezone.get_default_timezone()


class Rate(models.Model):
    created = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
    currency_type = models.PositiveSmallIntegerField(choices=mch.CURRENCY_TYPE_CHOICES)
    type = models.PositiveSmallIntegerField(choices=mch.RATE_TYPE_CHOICES) # noqa

    def save(self, *args, **kwargs):
        self.amount = to_decimal(self.amount)
        super().save(*args, **kwargs)

    def datetime_str(self):
        return f'{self.created.astimezone(time_zone).strftime("%d.%m.%Y %H:%M")}'
