from django.contrib import admin

from .models import Rate, PeriodRate, Payment


@admin.register(Rate)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    list_filter = ['name']


@admin.register(PeriodRate)
class PeriodRateAdmin(admin.ModelAdmin):
    list_display = ['rate', 'day', 'start_time', 'end_time', ]
    list_filter = ['day']
