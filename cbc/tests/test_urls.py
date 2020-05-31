from django.test import SimpleTestCase
from django.urls import reverse_lazy, resolve

from cbc.views.general import (
    HomeView,
    CBCListView,
    CBCDeleteView,
    CommonChartsTemplateView,
    DiffChartsTemplateView,
    IndexChartsTemplateView
)
from cbc.views.three_diff import ThreeDifCreateView, ThreeDifUpdateView, ThreeDifDetailView
from cbc.views.five_diff import FiveDifCreateView, FiveDifUpdateView, FiveDifDetailView
from cbc.views.blood_smear import BloodSmearCreateView, BloodSmearUpdateView, BloodSmearDetailView


class TestUrlsGeneral(SimpleTestCase):

    def test_url_home(self):
        url = reverse_lazy('cbc:home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_url_cbc_list(self):
        url = reverse_lazy('cbc:cbc-list')
        self.assertEqual(resolve(url).func.view_class, CBCListView)

    def test_url_cbc_delete(self):
        url = reverse_lazy('cbc:cbc-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, CBCDeleteView)


class TestUrlsChart(SimpleTestCase):

    def test_url_cbc_chart_common(self):
        url = reverse_lazy('cbc:cbc-charts-common')
        self.assertEqual(resolve(url).func.view_class, CommonChartsTemplateView)

    def test_url_cbc_chart_diff(self):
        url = reverse_lazy('cbc:cbc-charts-diff')
        self.assertEqual(resolve(url).func.view_class, DiffChartsTemplateView)

    def test_url_cbc_chart_index(self):
        url = reverse_lazy('cbc:cbc-charts-index')
        self.assertEqual(resolve(url).func.view_class, IndexChartsTemplateView)


class TestUrlsThreeDiff(SimpleTestCase):

    def test_url_cbc_three_diff_create(self):
        url = reverse_lazy('cbc:three-dif-create')
        self.assertEqual(resolve(url).func.view_class, ThreeDifCreateView)

    def test_url_cbc_three_diff_detail(self):
        url = reverse_lazy('cbc:three-dif-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ThreeDifDetailView)

    def test_url_cbc_three_diff_update(self):
        url = reverse_lazy('cbc:three-dif-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ThreeDifUpdateView)


class TestUrlsFiveDiff(SimpleTestCase):

    def test_url_cbc_five_diff_create(self):
        url = reverse_lazy('cbc:five-dif-create')
        self.assertEqual(resolve(url).func.view_class, FiveDifCreateView)

    def test_url_cbc_five_diff_detail(self):
        url = reverse_lazy('cbc:five-dif-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, FiveDifDetailView)

    def test_url_cbc_five_diff_update(self):
        url = reverse_lazy('cbc:five-dif-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, FiveDifUpdateView)


class TestUrlsBloodSmear(SimpleTestCase):

    def test_url_cbc_blood_smear_create(self):
        url = reverse_lazy('cbc:blood-smear-create')
        self.assertEqual(resolve(url).func.view_class, BloodSmearCreateView)

    def test_url_cbc_blood_smear_detail(self):
        url = reverse_lazy('cbc:blood-smear-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, BloodSmearDetailView)

    def test_url_cbc_blood_smear_update(self):
        url = reverse_lazy('cbc:blood-smear-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, BloodSmearUpdateView)
