from django.contrib.auth.decorators import login_required
from django.urls import path

from cbc.views.general import (
    HomeView,
    CBCListView,
    CBCDeleteView,
    CommonChartsTemplateView,
    IndexChartsTemplateView,
    DiffChartsTemplateView
)
from cbc.views.three_diff import ThreeDifCreateView, ThreeDifUpdateView, ThreeDifDetailView
from cbc.views.five_diff import FiveDifCreateView, FiveDifUpdateView, FiveDifDetailView
from cbc.views.blood_smear import BloodSmearCreateView, BloodSmearUpdateView, BloodSmearDetailView


app_name = 'cbc'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('cbc/', login_required(CBCListView.as_view()), name='cbc-list'),
    path('cbc/<int:id>/delete/', login_required(CBCDeleteView.as_view()), name='cbc-delete'),

    path('cbc/charts-common', login_required(CommonChartsTemplateView.as_view()), name='cbc-charts-common'),
    path('cbc/charts-diff', login_required(DiffChartsTemplateView.as_view()), name='cbc-charts-diff'),
    path('cbc/charts-index', login_required(IndexChartsTemplateView.as_view()), name='cbc-charts-index'),

    path('cbc/three-dif/create/', ThreeDifCreateView.as_view(), name='three-dif-create'),
    path('cbc/three-dif/<int:pk>', ThreeDifDetailView.as_view(), name='three-dif-detail'),
    path('cbc/three-dif/<int:pk>/update/', login_required(ThreeDifUpdateView.as_view()), name='three-dif-update'),

    path('cbc/five-dif/create/', FiveDifCreateView.as_view(), name='five-dif-create'),
    path('cbc/five-dif/<int:pk>', FiveDifDetailView.as_view(), name='five-dif-detail'),
    path('cbc/five-dif/<int:pk>/update/', login_required(FiveDifUpdateView.as_view()), name='five-dif-update'),

    path('cbc/blood-smear/create/', BloodSmearCreateView.as_view(), name='blood-smear-create'),
    path('cbc/blood-smear/<int:pk>', BloodSmearDetailView.as_view(), name='blood-smear-detail'),
    path('cbc/blood-smear/<int:pk>/update/', login_required(BloodSmearUpdateView.as_view()), name='blood-smear-update')
]
