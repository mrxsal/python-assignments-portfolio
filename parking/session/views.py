
import datetime

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import make_aware
from django.views.generic import CreateView, DetailView, FormView

from .forms import ParkingLotForm, ReservationForm
from .models import ParkingSpace, Session
from accounts.models import Vehicle


class ParkingLotView(FormView):
    model = ParkingSpace
    template_name = 'session/parking-lot.html'
    form_class = ParkingLotForm

    def get_queryset(self):
        lots = ParkingSpace.objects.all()
        return lots

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parking_spaces'] = self.get_parking_lots()
        context['current_occupancy'] = self.get_current_occupancy()
        return context

    def get_form_kwargs(self):
        kwargs = super(ParkingLotView, self).get_form_kwargs()
        kwargs['floor'] = self.request.GET.get('floor', 1)
        return kwargs

    def get_parking_lots(self):
        floor = self.request.GET.get('floor', 1)
        parking_spaces = ParkingSpace.objects.filter(
            floor=floor).order_by('code')
        return parking_spaces

    def get_current_occupancy(self):
        all_parking_spaces = ParkingSpace.objects.all().count()
        unavailable_parking_spaces = ParkingSpace.objects.filter(
            Q(session__start__lte=make_aware(datetime.datetime.now())) &
            Q(session__end__gte=make_aware(datetime.datetime.now()))).count()
        if not all_parking_spaces:
            return 'No Parking Spaces'
        return f'{round(unavailable_parking_spaces / all_parking_spaces, 2)*100}%'


class ReservationView(CreateView):
    model = Session
    template_name = 'session/reservation.html'
    form_class = ReservationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        vehicle, created = Vehicle.objects.get_or_create(license_plate=form.cleaned_data.get(
            'license_plate').upper().replace(' ', '').replace('-', ''))
        self.object.vehicle = vehicle
        if self.find_parking_space():
            parking_space = self.find_parking_space()
        else:
            return HttpResponseRedirect(self.request.path_info)
        self.object.parking_space = parking_space
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('reservation-success', args=[self.object.id])

    def find_parking_space(self):
        empty_parking_space = ParkingSpace.objects.filter(
            ~(Q(session__start__lte=self.object.end) &
              Q(session__end__gte=self.object.start)))
        if empty_parking_space.exists():
            return empty_parking_space[0]
        messages.error(
            self.request, 'There are no available spaces for the selected time slots.')
        return None


class ReservationSuccessView(DetailView):
    model = Session
    pk_url_kwarg = 'id'
    template_name = 'session/reservation-success.html'
