import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy

from cbc.models import CompleteBloodCount, BloodSmear
from patient.models import Patient
from patient.views import EditProfileView


class TestViewsPatient(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

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
        self.cbc_blood_smear = CompleteBloodCount.objects.create(
            user=self.user,
            sex=self.user.patient.sex,
            age=self.user.patient.get_age(),
            analysis_date=datetime.date(2020, 4, 29),
            leukocyte=2,
            erythrocyte=2,
            hemoglobin=2,
            hematocrit=2,
            sed_rate=2,
            type=2,
            sum=100,
            object_id=1,
            content_type_id=9
        )
        self.blood_smear = BloodSmear.objects.create(
            cbc=self.cbc_blood_smear,
            value_type='absolute',
            promyelocyte=3,
            myelocyte=3,
            metamyelocyte=3,
            banded_neutrophil=3,
            segmented_neutrophil=3,
            lymphocyte=3,
            monocyte=3,
            eosinophil=3,
            basophil=3,
            plasma_cell=3
        )

        self.url_patient_edit_profile = reverse_lazy('patient:edit_profile', args=[self.patient.pk])

    def tearDown(self):
        self.user.delete()
        self.patient.delete()
        self.cbc_blood_smear.delete()
        self.blood_smear.delete()

    def test_view_patient_edit_profile(self):
        new_data = {
            'firstname': 'john',
            'lastname': 'doe'
        }

        request = self.factory.post(self.url_patient_edit_profile, new_data)
        request.user = self.user
        response = EditProfileView.as_view()(request, pk=self.patient.pk)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )
