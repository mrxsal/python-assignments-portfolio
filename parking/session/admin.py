from django.contrib import admin

from .models import ParkingLot, Session


@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ['code', 'floor']
    list_filter = ['code']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'parking_lot', 'start',
                    'end', 'check_in', 'check_out', 'is_active']
