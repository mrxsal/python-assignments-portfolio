from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from .models import ParkingSpace, Session
from .views import ReservationView
from accounts.models import Vehicle
from parking.tests import BaseTestCaseSetup


class ReservationTest(BaseTestCaseSetup, TestCase):
    def test_get_reservation(self):
        request = self.rf.get(reverse('reservation'))
        response = ReservationView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_reservation(self):
        data = {
            "session_type": "reservation",
            "start": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "end": (datetime.now()+timedelta(hours=1)).strftime('%d/%m/%Y %H:%M'),
            "license_plate": "T00G3THR"
        }
        request = self.rf.post(reverse('reservation'), data=data)
        response = ReservationView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Session.objects.filter(
            vehicle__license_plate="T00G3THR").exists(), True)

    def test_create_session(self):
        self.assertEqual(Session.objects.all().count(), 6)
        parking_space = ParkingSpace.objects.first()  # 1B
        self.assertEqual(parking_space.session_set.count(), 0)

        created_ses = Session.objects.create(
            vehicle=Vehicle.objects.first(),
            parking_space=parking_space,
            session_type="Reservation",
            start=make_aware(datetime.now()),
            end=make_aware(datetime.now() + timedelta(hours=1))
        )
        self.assertEqual(Session.objects.all().count(), 7)
        self.assertEqual(parking_space.session_set.first(), created_ses)

    def test_overlapping_sessions(self):
        base_session = Session.objects.first()
        no_overlap = Session(
            vehicle=Vehicle.objects.last(),
            parking_space=base_session.parking_space,
            session_type="reservation",
            start=base_session.end+timedelta(minutes=1),
            end=base_session.end+timedelta(hours=1),
        )
        self.assertEqual(no_overlap.full_clean(), None)
        overlap1 = Session(
            vehicle=Vehicle.objects.last(),
            parking_space=base_session.parking_space,
            session_type="reservation",
            start=base_session.start+timedelta(minutes=1),
            end=base_session.end+timedelta(minutes=1),
        )
        self.assertRaises(ValidationError, overlap1.full_clean)
        overlap2 = Session(
            vehicle=Vehicle.objects.last(),
            parking_space=base_session.parking_space,
            session_type="reservation",
            start=base_session.start-timedelta(minutes=1),
            end=base_session.end+timedelta(minutes=1),
        )
        self.assertRaises(ValidationError, overlap2.full_clean)
        overlap3 = Session(
            vehicle=Vehicle.objects.last(),
            parking_space=base_session.parking_space,
            session_type="reservation",
            start=base_session.start+timedelta(minutes=1),
            end=base_session.end-timedelta(minutes=1),
        )
        self.assertRaises(ValidationError, overlap3.full_clean)
        overlap4 = Session(
            vehicle=Vehicle.objects.last(),
            parking_space=base_session.parking_space,
            session_type="reservation",
            start=base_session.start-timedelta(minutes=1),
            end=base_session.end-timedelta(minutes=1),
        )
        self.assertRaises(ValidationError, overlap4.full_clean)

    def test_end_date_after_start_date(self):
        created_ses = Session(
            vehicle=Vehicle.objects.last(),
            parking_space=ParkingSpace.objects.first(),
            session_type="reservation",
            start=make_aware(datetime.now()),
            end=datetime.now()-timedelta(hours=1),
        )
        self.assertRaises(ValidationError, created_ses.full_clean)


class ParkingSpaceTest(BaseTestCaseSetup, TestCase):

    def test_create_parking_space(self):
        # after migration there should be 30 demo parking spaces
        self.assertEqual(30, ParkingSpace.objects.all().count())
        ParkingSpace.objects.create(
            code="AA123XX",
            floor=1
        )
        self.assertEqual(True, ParkingSpace.objects.filter(
            code="AA123XX").exists())
