import datetime

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    def set_initial_rates(apps, schema_editor):
        Rate = apps.get_model('payments', 'Rate')
        for i, name in enumerate(['free', 'standard', 'premium']):
            Rate.objects.create(
                name=name,
                value=i,
                currency='euro'
            )

    def set_initial_period_rates(app, schema_editor):
        PeriodRate = app.get_model('payments', 'PeriodRate')
        Rate = app.get_model('payments', 'Rate')
        for i in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            PeriodRate.objects.create(
                rate=Rate.objects.get(id=2),
                day=i,
                start_time=datetime.time(hour=8),
                end_time=datetime.time(hour=23)
            )

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('not_required', 'Not Required'), ('not_started', 'Not Started'), (
                    'pending', 'Pending'), ('declined', 'Declined'), ('completed', 'Completed')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('currency', models.CharField(choices=[
                 ('euro', 'euro')], default='euro', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), (
                    'thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=10)),
                ('start_time', models.TimeField(choices=[(datetime.time(0, 0), '00:00'), (datetime.time(1, 0), '01:00'), (datetime.time(2, 0), '02:00'), (datetime.time(3, 0), '03:00'), (datetime.time(4, 0), '04:00'), (datetime.time(5, 0), '05:00'), (datetime.time(6, 0), '06:00'), (datetime.time(7, 0), '07:00'), (datetime.time(8, 0), '08:00'), (datetime.time(9, 0), '09:00'), (datetime.time(10, 0), '10:00'), (datetime.time(
                    11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00'), (datetime.time(18, 0), '18:00'), (datetime.time(19, 0), '19:00'), (datetime.time(20, 0), '20:00'), (datetime.time(21, 0), '21:00'), (datetime.time(22, 0), '22:00'), (datetime.time(23, 0), '23:00')])),
                ('end_time', models.TimeField(choices=[(datetime.time(0, 0), '00:00'), (datetime.time(1, 0), '01:00'), (datetime.time(2, 0), '02:00'), (datetime.time(3, 0), '03:00'), (datetime.time(4, 0), '04:00'), (datetime.time(5, 0), '05:00'), (datetime.time(6, 0), '06:00'), (datetime.time(7, 0), '07:00'), (datetime.time(8, 0), '08:00'), (datetime.time(9, 0), '09:00'), (datetime.time(10, 0), '10:00'), (datetime.time(
                    11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00'), (datetime.time(18, 0), '18:00'), (datetime.time(19, 0), '19:00'), (datetime.time(20, 0), '20:00'), (datetime.time(21, 0), '21:00'), (datetime.time(22, 0), '22:00'), (datetime.time(23, 0), '23:00')])),
                ('rate', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='payments.rate')),
            ],
        ),
        migrations.RunPython(set_initial_rates),
        migrations.RunPython(set_initial_period_rates),
    ]
