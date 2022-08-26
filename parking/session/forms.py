from datetime import datetime, timedelta

from django import forms

from .models import ParkingSpace, Session


class ParkingLotForm(forms.ModelForm):
    def get_floor_choices():
        floors = ParkingSpace.objects.all().values_list('floor', flat=True).distinct()
        CHOICES = [(i, i) for i in floors]
        return CHOICES

    floor = forms.ChoiceField(choices=get_floor_choices)

    class Meta:
        model = ParkingSpace
        fields = ['floor']


class ReservationForm(forms.ModelForm):
    license_plate = forms.CharField(max_length=10)
    start = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'], initial=datetime.now())
    end = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'], initial=datetime.now() + timedelta(hours=1))

    class Meta:
        model = Session
        fields = ['session_type', 'start', 'end']
