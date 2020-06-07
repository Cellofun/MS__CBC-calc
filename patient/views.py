from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from .forms import RegistrationForm, EditProfileForm
from .models import Patient
from cbc.models import CompleteBloodCount, BloodSmear


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
        context['cbc'] = CompleteBloodCount.objects.filter(user=self.request.user)
        context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=self.request.user)
        return context

    def form_valid(self, form):
        with transaction.atomic():
            CompleteBloodCount.objects\
                .filter(user=self.request.user)\
                .update(age=self.request.user.patient.get_age(), sex=self.request.user.patient.sex)
        return super(EditProfileView, self).form_valid(form)


class TOSView(TemplateView):
    template_name = 'registration/tos.html'
