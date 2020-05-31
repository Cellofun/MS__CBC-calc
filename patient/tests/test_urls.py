from django.test import SimpleTestCase
from django.urls import reverse_lazy, resolve

from django.contrib.auth.views import LoginView
from patient.views import RegisterView, EditProfileView


class TestUrls(SimpleTestCase):

    def test_url_patient_login(self):
        url = reverse_lazy('patient:login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_url_patient_register(self):
        url = reverse_lazy('patient:register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_url_patient_edit_profile(self):
        url = reverse_lazy('patient:edit_profile', args=[1])
        self.assertEqual(resolve(url).func.view_class, EditProfileView)
