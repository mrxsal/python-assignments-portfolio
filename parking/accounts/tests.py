from django.test import TestCase

from .models import Vehicle
from parking.tests import BaseTestCaseSetup


class VehicleTest(BaseTestCaseSetup, TestCase):

    def test_processing_license_plate(self):
        space1 = Vehicle.objects.create(
            license_plate="aa-123 Xa",
        )
        self.assertEqual(space1.license_plate, 'AA123XA')
