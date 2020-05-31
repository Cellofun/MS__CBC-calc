import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from cbc.forms import ThreeDiffFormSet, FiveDiffFormSet, BloodSmearFormSet
from patient.models import Patient


class TestFormsCBC(TestCase):

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

    def test_form_is_valid_three_diff(self):
        form = ThreeDiffFormSet(
            data={
                "three_diff-INITIAL_FORMS": 0,
                "three_diff-TOTAL_FORMS": 1,
                "three_diff-MAX_NUM_FORMS": '',
                "three_diff-0-value_type": "relative",
                "three_diff-0-neutrophil": 1.0,
                "three_diff-0-lymphocyte": 1.0,
                "three_diff-0-monocyte": 1.0,
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_is_valid_five_diff(self):
        form = FiveDiffFormSet(
            data={
                "five_diff-INITIAL_FORMS": 0,
                "five_diff-TOTAL_FORMS": 1,
                "five_diff-MAX_NUM_FORMS": '',
                "five_diff-0-value_type": "relative",
                "five_diff-0-neutrophil": 1.0,
                "five_diff-0-lymphocyte": 1.0,
                "five_diff-0-monocyte": 1.0,
                "five_diff-0-eosinophil": 1.0,
                "five_diff-0-basophil": 1.0,
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_is_valid_blood_smear(self):
        form = BloodSmearFormSet(
            data={
                "blood_smear-INITIAL_FORMS": 0,
                "blood_smear-TOTAL_FORMS": 1,
                "blood_smear-MAX_NUM_FORMS": '',
                "blood_smear-0-value_type": "relative",
                "blood_smear-0-promyelocyte": 1.0,
                "blood_smear-0-myelocyte": 1.0,
                "blood_smear-0-metamyelocyte": 1.0,
                "blood_smear-0-banded_neutrophil": 1.0,
                "blood_smear-0-segmented_neutrophil": 1.0,
                "blood_smear-0-lymphocyte": 1.0,
                "blood_smear-0-monocyte": 1.0,
                "blood_smear-0-eosinophil": 1.0,
                "blood_smear-0-basophil": 1.0,
                "blood_smear-0-plasma_cell": 1.0,
            }
        )
        self.assertTrue(form.is_valid())
