import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from cbc.models import CompleteBloodCount, BloodSmear
from patient.models import Patient


class TestModel(TestCase):

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
        self.cbc = CompleteBloodCount.objects.create(
            user=self.user,
            sex=self.user.patient.sex,
            age=self.user.patient.get_age(),
            analysis_date=datetime.date(2020, 4, 29),
            leukocyte=10.5,
            erythrocyte=3.5,
            hemoglobin=110,
            hematocrit=33,
            sed_rate=4,
            type=9,
            content_type_id=7,
            object_id=1,
            sum=100
        )

    def tearDown(self):
        self.user.delete()
        self.patient.delete()
        self.cbc.delete()

    def test_model_index_intoxicationKK_relative(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='relative',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=4,
            segmented_neutrophil=66,
            lymphocyte=22,
            monocyte=8,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.intoxicationKK(), 2.47)

    def test_model_index_intoxicationO_relative(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='relative',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=4,
            segmented_neutrophil=66,
            lymphocyte=22,
            monocyte=8,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.intoxicationO(), 2.33)

    def test_model_index_nuclear_relative(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='relative',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=4,
            segmented_neutrophil=66,
            lymphocyte=22,
            monocyte=8,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.nuclear(), 0.18)

    def test_model_index_shift_relative(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='relative',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=4,
            segmented_neutrophil=66,
            lymphocyte=22,
            monocyte=8,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.shift(), 3.18)

    def test_model_index_allergy_relative(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='relative',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=4,
            segmented_neutrophil=66,
            lymphocyte=22,
            monocyte=8,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.allergy(), 0.41)

    def test_model_index_intoxicationKK_absolute(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='absolute',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=0.42,
            segmented_neutrophil=6.93,
            lymphocyte=2.31,
            monocyte=0.84,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.intoxicationKK(), 2.47)

    def test_model_index_intoxicationO_absolute(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='absolute',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=0.42,
            segmented_neutrophil=6.93,
            lymphocyte=2.31,
            monocyte=0.84,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.intoxicationO(), 2.33)

    def test_model_index_nuclear_absolute(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='absolute',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=0.42,
            segmented_neutrophil=6.93,
            lymphocyte=2.31,
            monocyte=0.84,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.nuclear(), 0.18)

    def test_model_index_shift_absolute(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='absolute',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=0.42,
            segmented_neutrophil=6.93,
            lymphocyte=2.31,
            monocyte=0.84,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.shift(), 3.18)

    def test_model_index_allergy_absolute(self):
        blood_smear = BloodSmear.objects.create(
            cbc=self.cbc,
            value_type='absolute',
            promyelocyte=0,
            myelocyte=0,
            metamyelocyte=0,
            banded_neutrophil=0.42,
            segmented_neutrophil=6.93,
            lymphocyte=2.31,
            monocyte=0.84,
            eosinophil=0,
            basophil=0,
            plasma_cell=0
        )
        self.assertEqual(blood_smear.allergy(), 0.41)
