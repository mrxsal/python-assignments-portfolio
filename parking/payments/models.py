import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Rate(models.Model):
    CURRENCY_CHOICES = [('euro', 'euro')]

    name = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(
        max_length=10, choices=CURRENCY_CHOICES, default="euro")


class PeriodRate(models.Model):
    class DayChoices(models.TextChoices):
        MONDAY = "monday", _("Monday")
        TUESDAY = "tuesday", _("Tuesday")
        WEDNESDAY = "wednesday", _("Wednesday")
        THURSDAY = "thursday", _("Thursday")
        FRIDAY = "friday", _("Friday")
        SATURDAY = "saturday", _("Saturday")
        SUNDAY = "sunday", _("Sunday")

    HOUR_CHOICES = [
        (datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

    rate = models.ForeignKey(Rate, on_delete=models.CASCADE, null=False)
    day = models.CharField(max_length=10, choices=DayChoices.choices)
    start_time = models.TimeField(choices=HOUR_CHOICES, null=False)
    end_time = models.TimeField(choices=HOUR_CHOICES, null=False)

    def clean(self):
        super().clean()
        rateday = PeriodRate.objects.filter(rate=self.rate, day=self.day)
        if rateday.filter(start_time__lte=self.start_time, end_time__gte=self.end_time):
            raise ValidationError('Overlapping start and end-times for this day and rate combination.')


class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        NOT_REQUIRED = "not_required", _("Not Required")
        NOT_STARTED = "not_started", _("Not Started")
        PENDING = "pending", _("Pending")
        DECLINED = "declined", _("Declined")
        COMPLETED = "completed", _("Completed")
    
    status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices)