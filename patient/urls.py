from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import path

from .views import RegisterView, EditProfileView


app_name = 'patient'

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/profile/<int:pk>/edit/', login_required(EditProfileView.as_view()), name='edit_profile'),
]
