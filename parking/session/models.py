
import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class ParkingSpace(models.Model):
    code = models.CharField(max_length=8, null=False, unique=True)
    floor = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.code

    @property
    def active_session(self, _datetime=datetime.datetime.now()):
        session = self.session_set.filter(
            start__lte=_datetime, end__gte=_datetime)
        if session.exists():
            return session[0]
        return None

    @property
    def is_taken(self, _datetime=datetime.datetime.now()):
        if self.active_session:
            return True
        return False


class Session(models.Model):
    class SessionType(models.TextChoices):
        RESERVATION = "reservation", _("Reservation")
        ON_ARRIVAL = "on_arrival", _("On Arrival")

    vehicle = models.ForeignKey('accounts.vehicle', on_delete=models.CASCADE)
    parking_space = models.ForeignKey(
        ParkingSpace, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        'payments.payment', on_delete=models.CASCADE, null=True, blank=True)

    session_type = models.CharField(
        'session type', choices=SessionType.choices, max_length=15, default="on_arrival")

    # start/end of either reservation or prepaid
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    # actual start/end of parking session
    check_in = models.DateTimeField('check in', null=True, blank=True)
    check_out = models.DateTimeField('check out', null=True, blank=True)

    is_active = models.BooleanField(default=False, null=False)

    def validate_on_clean_and_save(self):
        if Session.objects.filter(parking_space=self.parking_space, start__lte=self.end, end__gte=self.start):
            raise ValidationError(
                'This parking lot already has an active reservation for this start and end date.')
        if self.end <= self.start:
            raise ValidationError('start date comes after the end date.')

    def clean(self):
        super().clean()
        self.validate_on_clean_and_save()

    def save(self, *args, **kwargs):
        self.validate_on_clean_and_save()
        super(Session, self).save(*args, **kwargs)
