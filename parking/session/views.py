
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView

from .forms import ReservationForm, ParkingLotForm
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
        return context

    def get_parking_lots(self):
        floor = self.request.GET.get('floor', 1)
        parking_spaces = ParkingSpace.objects.filter(
            floor=floor).order_by('code')
        return parking_spaces


class ReservationView(CreateView):
    model = Session
    template_name = 'session/reservation.html'
    form_class = ReservationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        vehicle, created = Vehicle.objects.get_or_create(
            license_plate=form.cleaned_data.get('license_plate'))
        self.object.vehicle = vehicle
        parking_space = self.find_parking_space()
        self.object.parking_space = parking_space
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('reservation-success', args=[self.object.id])

    def find_parking_space(self):
        empty_parking_space = ParkingSpace.objects.filter(
            ~Q(session__start__lte=self.object.start) &
            ~Q(session__end__gte=self.object.end))
        if empty_parking_space.exists():
            return empty_parking_space[0]
        return HttpResponseRedirect(self.request.path_info)


class ReservationSuccessView(DetailView):
    model = Session
    pk_url_kwarg = 'id'
    template_name = 'session/reservation-success.html'
