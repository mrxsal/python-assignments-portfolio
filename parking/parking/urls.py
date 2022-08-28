from django.conf import settings
from django.contrib import admin
from django.urls import path

from session.views import ParkingLotView, ReservationView, ReservationSuccessView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', ParkingLotView.as_view(), name='parkinglot'),
    path('reservation/', ReservationView.as_view(), name='reservation'),
    path('reservation/<int:id>/', ReservationSuccessView.as_view(),
         name='reservation-success'),
]
