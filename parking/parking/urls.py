from django.conf import settings
from django.contrib import admin
from django.urls import path

from session.views import ParkingLotView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ParkingLotView.as_view(), name='parkinglot'), 
]
# if settings.DEBUG:
#     from django.conf.urls.static import static
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
