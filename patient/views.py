from django.urls import reverse_lazy
from django.views import generic

from .forms import LoginForm, RegistrationForm, EditProfileForm
from .models import Patient
from cbc.models import CompleteBloodCount, BloodSmear


class LoginView(generic.FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RegisterView(generic.FormView):
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    success_url = '/accounts/login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EditProfileView(generic.UpdateView):
    model = Patient
    form_class = EditProfileForm
    template_name = 'patient/edit_profile.html'
    success_url = reverse_lazy('cbc:cbc-list')

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(user=self.request.user)
        context['cbc'] = CompleteBloodCount.objects.filter(user=self.request.user)
        context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=self.request.user)
        return context
