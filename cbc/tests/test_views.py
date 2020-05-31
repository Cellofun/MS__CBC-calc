import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy

from cbc.models import CompleteBloodCount, BloodSmear, FiveDiff, ThreeDiff
from patient.models import Patient
from range.models import ReferenceRange, DiffRange, CBCRange

from cbc.views.general import (
    CBCListView,
    CBCDeleteView,
    CommonChartsTemplateView,
    DiffChartsTemplateView,
    IndexChartsTemplateView
)
from cbc.views.three_diff import ThreeDifCreateView, ThreeDifUpdateView, ThreeDifDetailView
from cbc.views.five_diff import FiveDifCreateView, FiveDifUpdateView, FiveDifDetailView
from cbc.views.blood_smear import BloodSmearCreateView, BloodSmearUpdateView, BloodSmearDetailView


class TestViewsGeneral(TestCase):

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

        self.cbc_three_diff = CompleteBloodCount.objects.create(
            user=self.user,
            sex=self.user.patient.sex,
            age=self.user.patient.get_age(),
            analysis_date=datetime.date(2020, 4, 30),
            leukocyte=1,
            erythrocyte=1,
            hemoglobin=1,
            hematocrit=1,
            sed_rate=1,
            type=3,
            sum=100,
            object_id=1,
            content_type_id=10
        )
        self.cbc_five_diff = CompleteBloodCount.objects.create(
            sex='female',
            age=28,
            analysis_date=datetime.date(2020, 4, 28),
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
        self.three_diff = ThreeDiff.objects.create(
            cbc=self.cbc_three_diff,
            value_type='relative',
            neutrophil=1,
            lymphocyte=1,
            monocyte=1
        )
        self.five_diff = FiveDiff.objects.create(
            cbc=self.cbc_five_diff,
            value_type='absolute',
            neutrophil=2,
            lymphocyte=2,
            monocyte=2,
            eosinophil=2,
            basophil=2
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

        self.url_login = reverse_lazy('patient:login')
        self.url_home = reverse_lazy('cbc:home')
        self.url_cbc_list = reverse_lazy('cbc:cbc-list')
        self.url_cbc_delete = reverse_lazy('cbc:cbc-delete', args=[self.cbc_blood_smear.pk])
        self.url_cbc_chart_common = reverse_lazy('cbc:cbc-charts-common')
        self.url_cbc_chart_diff = reverse_lazy('cbc:cbc-charts-diff')
        self.url_cbc_chart_index = reverse_lazy('cbc:cbc-charts-index')

    def tearDown(self):
        self.user.delete()
        self.patient.delete()
        self.cbc_three_diff.delete()
        self.three_diff.delete()
        self.cbc_five_diff.delete()
        self.five_diff.delete()
        self.cbc_blood_smear.delete()
        self.blood_smear.delete()

    def test_view_home(self):
        response = self.client.get(self.url_home)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_view_cbc_list(self):
        request = self.factory.get(self.url_cbc_list)
        request.user = self.user
        response = CBCListView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('object_list'),
            map(repr, [self.cbc_three_diff, self.cbc_blood_smear])
        )
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

    def test_view_cbc_delete(self):
        request = self.factory.get(self.url_cbc_delete)
        request.user = self.user
        response = CBCDeleteView.as_view()(request, pk=self.cbc_blood_smear.pk)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

        post_request = self.factory.post(self.url_cbc_delete)
        post_request.user = self.user
        post_response = CBCDeleteView.as_view()(post_request, pk=self.cbc_blood_smear.pk)
        self.assertEqual(post_response.status_code, 302)

    def test_view_cbc_chart_common(self):
        request = self.factory.get(self.url_cbc_chart_common)
        request.user = self.user
        response = CommonChartsTemplateView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('cbc'),
            map(repr, [self.cbc_three_diff, self.cbc_blood_smear])
        )
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

    def test_view_cbc_chart_diff(self):
        request = self.factory.get(self.url_cbc_chart_diff)
        request.user = self.user
        response = DiffChartsTemplateView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('cbc'),
            map(repr, [self.cbc_three_diff, self.cbc_blood_smear])
        )

        self.assertQuerysetEqual(
            response.context_data.get('three_dif'),
            map(repr, [self.three_diff])
        )
        self.assertQuerysetEqual(
            response.context_data.get('five_dif'), []
        )
        self.assertQuerysetEqual(
            response.context_data.get('blood_smear'),
            map(repr, [self.blood_smear])
        )
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

    def test_view_cbc_chart_index(self):
        request = self.factory.get(self.url_cbc_chart_index)
        request.user = self.user
        response = IndexChartsTemplateView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('cbc'),
            map(repr, [self.cbc_three_diff, self.cbc_blood_smear])
        )
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )


class TestViewsThreeDiff(TestCase):

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

        self.cbc_three_diff = CompleteBloodCount.objects.create(
            user=self.user,
            sex=self.user.patient.sex,
            age=self.user.patient.get_age(),
            analysis_date=datetime.date(2020, 4, 30),
            leukocyte=1,
            erythrocyte=1,
            hemoglobin=1,
            hematocrit=1,
            sed_rate=1,
            type=3,
            sum=100,
            object_id=1,
            content_type_id=10
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
        self.three_diff = ThreeDiff.objects.create(
            cbc=self.cbc_three_diff,
            value_type='relative',
            neutrophil=1,
            lymphocyte=1,
            monocyte=1
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
        self.cbc_range = CBCRange.objects.create(
            sex='male',
            age_min=10,
            age_max=120,
            leukocyte_min=1,
            leukocyte_max=2,
            erythrocyte_min=1,
            erythrocyte_max=2,
            hemoglobin_min=1,
            hemoglobin_max=2,
            hematocrit_min=1,
            hematocrit_max=2,
            sed_rate_min=1,
            sed_rate_max=2
        )
        self.diff_range = DiffRange.objects.create(
            age_min=10,
            age_max=120,
            value_type='relative',
            promyelocyte_min=1,
            promyelocyte_max=2,
            myelocyte_min=1,
            myelocyte_max=2,
            metamyelocyte_min=1,
            metamyelocyte_max=2,
            banded_neutrophil_min=1,
            banded_neutrophil_max=2,
            segmented_neutrophil_min=1,
            segmented_neutrophil_max=2,
            neutrophil_min=1,
            neutrophil_max=2,
            lymphocyte_min=1,
            lymphocyte_max=2,
            monocyte_min=1,
            monocyte_max=2,
            eosinophil_min=1,
            eosinophil_max=2,
            basophil_min=1,
            basophil_max=2,
            plasma_cell_min=1,
            plasma_cell_max=2
        )
        self.reference_range = ReferenceRange.objects.create(
            cbc_id=self.cbc_range.pk,
            diff_id=self.diff_range.pk
        )

        self.url_cbc_three_diff_create = reverse_lazy('cbc:three-dif-create')
        self.url_cbc_three_diff_update = reverse_lazy('cbc:three-dif-update', args=[self.cbc_three_diff.pk])
        self.url_cbc_three_diff_detail = reverse_lazy('cbc:three-dif-detail', args=[self.cbc_three_diff.pk])

    def tearDown(self):
        self.user.delete()
        self.patient.delete()
        self.cbc_three_diff.delete()
        self.three_diff.delete()
        self.cbc_blood_smear.delete()
        self.blood_smear.delete()
        self.cbc_range.delete()
        self.diff_range.delete()
        self.reference_range.delete()

    def test_view_cbc_three_diff_create(self):
        new_three_diff = {
            'user': 'test',
            'analysis_date': '2020-05-05',
            'sum': 100,
            'value_type': 'relative',
            'neutrophil': 1,
            'lymphocyte': 1,
            'monocyte': 1
        }

        request = self.factory.post(self.url_cbc_three_diff_create, new_three_diff)
        request.user = self.user
        response = ThreeDifCreateView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

    def test_view_cbc_three_diff_update(self):
        new_three_diff = {
            'sum': 100,
            'neutrophil': 2,
            'lymphocyte': 2,
            'monocyte': 2
        }

        request = self.factory.post(self.url_cbc_three_diff_update, new_three_diff)
        request.user = self.user
        response = ThreeDifUpdateView.as_view()(request, pk=self.cbc_three_diff.pk)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

    def test_view_cbc_three_diff_detail(self):
        request = self.factory.get(self.url_cbc_three_diff_detail)
        request.user = self.user
        response = ThreeDifDetailView.as_view()(request, pk=self.cbc_three_diff.pk)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )


class TestViewsFiveDiff(TestCase):

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
        self.cbc_five_diff = CompleteBloodCount.objects.create(
            sex='female',
            age=28,
            analysis_date=datetime.date(2020, 4, 28),
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
        self.five_diff = FiveDiff.objects.create(
            cbc=self.cbc_five_diff,
            value_type='relative',
            neutrophil=2,
            lymphocyte=2,
            monocyte=2,
            eosinophil=2,
            basophil=2
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
        self.cbc_range = CBCRange.objects.create(
            sex='male',
            age_min=10,
            age_max=120,
            leukocyte_min=1,
            leukocyte_max=2,
            erythrocyte_min=1,
            erythrocyte_max=2,
            hemoglobin_min=1,
            hemoglobin_max=2,
            hematocrit_min=1,
            hematocrit_max=2,
            sed_rate_min=1,
            sed_rate_max=2
        )
        self.diff_range = DiffRange.objects.create(
            age_min=10,
            age_max=120,
            value_type='relative',
            promyelocyte_min=1,
            promyelocyte_max=2,
            myelocyte_min=1,
            myelocyte_max=2,
            metamyelocyte_min=1,
            metamyelocyte_max=2,
            banded_neutrophil_min=1,
            banded_neutrophil_max=2,
            segmented_neutrophil_min=1,
            segmented_neutrophil_max=2,
            neutrophil_min=1,
            neutrophil_max=2,
            lymphocyte_min=1,
            lymphocyte_max=2,
            monocyte_min=1,
            monocyte_max=2,
            eosinophil_min=1,
            eosinophil_max=2,
            basophil_min=1,
            basophil_max=2,
            plasma_cell_min=1,
            plasma_cell_max=2
        )
        self.reference_range = ReferenceRange.objects.create(
            cbc_id=self.cbc_range.pk,
            diff_id=self.diff_range.pk
        )

        self.url_cbc_five_diff_create = reverse_lazy('cbc:five-dif-create')
        self.url_cbc_five_diff_update = reverse_lazy('cbc:five-dif-update', args=[self.cbc_five_diff.pk])
        self.url_cbc_five_diff_detail = reverse_lazy('cbc:five-dif-detail', args=[self.cbc_five_diff.pk])

    def tearDown(self):
        self.user.delete()
        self.patient.delete()
        self.cbc_five_diff.delete()
        self.five_diff.delete()
        self.cbc_blood_smear.delete()
        self.blood_smear.delete()
        self.cbc_range.delete()
        self.diff_range.delete()
        self.reference_range.delete()

    def test_view_cbc_five_diff_create(self):
        new_five_diff = {
            'user': 'test',
            'analysis_date': '2020-05-05',
            'sum': 100,
            'value_type': 'relative',
            'neutrophil': 1,
            'lymphocyte': 1,
            'monocyte': 1,
            'eosinophil': 1,
            'basophil': 1
        }

        request = self.factory.post(self.url_cbc_five_diff_create, new_five_diff)
        request.user = self.user
        response = FiveDifCreateView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

    def test_view_cbc_five_diff_update(self):
        new_five_diff = {
            'sum': 100,
            'neutrophil': 3,
            'lymphocyte': 3,
            'monocyte': 3,
            'eosinophil': 3,
            'basophil': 3
        }

        request = self.factory.post(self.url_cbc_five_diff_update, new_five_diff)
        request.user = self.user
        response = FiveDifUpdateView.as_view()(request, pk=self.cbc_five_diff.pk)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

    def test_view_cbc_five_diff_detail(self):
        request = self.factory.get(self.url_cbc_five_diff_detail)
        request.user = self.user
        response = FiveDifDetailView.as_view()(request, pk=self.cbc_five_diff.pk)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )


class TestViewsBloodSmear(TestCase):

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
        self.cbc_range = CBCRange.objects.create(
            sex='male',
            age_min=10,
            age_max=120,
            leukocyte_min=1,
            leukocyte_max=2,
            erythrocyte_min=1,
            erythrocyte_max=2,
            hemoglobin_min=1,
            hemoglobin_max=2,
            hematocrit_min=1,
            hematocrit_max=2,
            sed_rate_min=1,
            sed_rate_max=2
        )
        self.diff_range = DiffRange.objects.create(
            age_min=10,
            age_max=120,
            value_type='absolute',
            promyelocyte_min=1,
            promyelocyte_max=2,
            myelocyte_min=1,
            myelocyte_max=2,
            metamyelocyte_min=1,
            metamyelocyte_max=2,
            banded_neutrophil_min=1,
            banded_neutrophil_max=2,
            segmented_neutrophil_min=1,
            segmented_neutrophil_max=2,
            neutrophil_min=1,
            neutrophil_max=2,
            lymphocyte_min=1,
            lymphocyte_max=2,
            monocyte_min=1,
            monocyte_max=2,
            eosinophil_min=1,
            eosinophil_max=2,
            basophil_min=1,
            basophil_max=2,
            plasma_cell_min=1,
            plasma_cell_max=2
        )
        self.reference_range = ReferenceRange.objects.create(
            cbc_id=self.cbc_range.pk,
            diff_id=self.diff_range.pk
        )

        self.url_cbc_blood_smear_create = reverse_lazy('cbc:blood-smear-create')
        self.url_cbc_blood_smear_update = reverse_lazy('cbc:blood-smear-update', args=[self.cbc_blood_smear.pk])
        self.url_cbc_blood_smear_detail = reverse_lazy('cbc:blood-smear-detail', args=[self.cbc_blood_smear.pk])

    def tearDown(self):
        self.user.delete()
        self.patient.delete()
        self.cbc_blood_smear.delete()
        self.blood_smear.delete()
        self.cbc_range.delete()
        self.diff_range.delete()
        self.reference_range.delete()

    def test_view_cbc_blood_smear_create(self):
        new_blood_smear = {
            'user': 'test',
            'analysis_date': '2020-05-05',
            'sum': 100,
            'value_type': 'absolute',
            'neutrophil': 1,
            'lymphocyte': 1,
            'monocyte': 1,
            'eosinophil': 1,
            'basophil': 1
        }

        request = self.factory.post(self.url_cbc_blood_smear_create, new_blood_smear)
        request.user = self.user
        response = BloodSmearCreateView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

    def test_view_cbc_blood_smear_update(self):
        new_blood_smear = {
            'sum': 100,
            'promyelocyte': 5,
            'myelocyte': 5,
            'metamyelocyte': 5,
            'anded_neutrophil': 5,
            'segmented_neutrophil': 5,
            'lymphocyte': 5,
            'monocyte': 5,
            'eosinophil': 5,
            'basophil': 5,
            'plasma_cell': 5
        }

        request = self.factory.post(self.url_cbc_blood_smear_update, new_blood_smear)
        request.user = self.user
        response = BloodSmearUpdateView.as_view()(request, pk=self.cbc_blood_smear.pk)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )

    def test_view_cbc_blood_smear_detail(self):
        request = self.factory.get(self.url_cbc_blood_smear_detail)
        request.user = self.user
        response = BloodSmearDetailView.as_view()(request, pk=self.cbc_blood_smear.pk)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context_data.get('blood_diagram'),
            map(repr, [self.blood_smear])
        )
