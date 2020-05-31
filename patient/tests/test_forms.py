import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from patient.forms import RegistrationForm
from patient.models import Patient


class TestFormsPatient(TestCase):

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
            date_of_birth=datetime.date(1990, 4, 25)
        )

    def tearDown(self):
        self.user.delete()
        self.patient.delete()

    def test_form_user_exists(self):
        age = datetime.date(1990, 4, 23)
        form = RegistrationForm(
            data={
                "username": "test",
                "password1": "qwety123",
                "password2": "qwety123",
                "email": "example@gmail.com",
                "date_of_birth": age,
                "sex": "male"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['username'], ['Пользователь с таким именем уже существует.'])

    def test_form_email_exists(self):
        age = datetime.date(1990, 4, 23)
        form = RegistrationForm(
            data={
                "username": "testo",
                "password1": "qwety123",
                "password2": "qwety123",
                "email": "test@gmail.com",
                "date_of_birth": age,
                "sex": "male"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'], ['Пользователь с таким email уже существует.'])
