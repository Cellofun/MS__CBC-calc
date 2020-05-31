from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from freezegun import freeze_time

from patient.models import Patient


class TestModelPatient(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='qwerty123',
            email='test@gmail.com'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            email=self.user.email,
            sex='male',
            date_of_birth=datetime(1990, 1, 12, 12, 0, 1)
        )

    def tearDown(self):
        self.user.delete()
        self.patient.delete()

    @freeze_time("2012-01-14")
    def test_model_patient_age(self):
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        assert datetime.now() == datetime(2012, 1, 14, 12, 0, 1)
        self.assertEqual(self.patient.get_age(), 22)
        freezer.stop()
