
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import ParkingLot, Session


class ParkingLotView(TemplateView):
    template_name = 'session/parking-lot.html'

    def get_queryset(self):
        sessions = ParkingLot.objects.all()
        return sessions
    
