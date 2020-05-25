from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from cbc.models import CompleteBloodCount, ThreeDiff, BloodSmear
from range.models import ReferenceRange
from patient.models import Patient

from cbc.forms import CBCModelForm, ThreeDiffFormSet


class ThreeDifCreateView(CreateView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_create.html'
    form_class = CBCModelForm

    def get_success_url(self):
        return reverse_lazy('cbc:three-dif-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ThreeDifCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['three_dif'] = ThreeDiffFormSet(self.request.POST)
        else:
            context['three_dif'] = ThreeDiffFormSet()
        if self.request.user.is_authenticated:
            context['patient'] = Patient.objects.get(user=self.request.user)
            context['blood_smear'] = BloodSmear.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        three_dif = context['three_dif']
        cbc = form.instance
        user = self.request.user
        with transaction.atomic():
            cbc.content_type = ContentType.objects.get(app_label='cbc', model='threediff')
            cbc.object_id = 0
            cbc.type = 3
            if user.is_authenticated:
                cbc.user = user

                patient = Patient.objects.get(user=user)
                cbc.age = patient.get_age()
                cbc.sex = patient.sex

            self.object = form.save()

            if three_dif.is_valid():
                three_dif.instance = self.object
                three_dif.save()

                fd_object = ThreeDiff.objects.get(cbc_id=self.object.id)
                cbc.object_id = fd_object.id

            self.object = form.save()

        return super(ThreeDifCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ThreeDifUpdateView(UpdateView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_update.html'
    form_class = CBCModelForm

    def get_success_url(self):
        return reverse_lazy('cbc:three-dif-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ThreeDifUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['three_dif'] = ThreeDiffFormSet(self.request.POST, instance=self.object)
        else:
            context['three_dif'] = ThreeDiffFormSet(instance=self.object)
        if self.request.user.is_authenticated:
            context['patient'] = Patient.objects.get(user=self.request.user)
            context['blood_smear'] = BloodSmear.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        three_dif = context['three_dif']
        with transaction.atomic():
            self.object = form.save()

            if three_dif.is_valid():
                three_dif.instance = self.object
                three_dif.save()

        return super(ThreeDifUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ThreeDifDetailView(DetailView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ThreeDifDetailView, self).get_context_data(**kwargs)
        three_diff = ThreeDiff.objects.get(cbc_id=self.object.id)
        context['three_dif'] = three_diff
        if self.request.user.is_authenticated:
            context['blood_smear'] = BloodSmear.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
            patient = Patient.objects.get(user=self.request.user)
            age = patient.get_age()
            context['patient'] = patient
            context['range'] = ReferenceRange.objects.get(
                cbc__sex=patient.sex,
                cbc__age_min__lt=age,
                cbc__age_max__gt=age,
                diff__value_type=three_diff.value_type
            )
        else:
            context['range'] = ReferenceRange.objects.get(
                cbc__sex=three_diff.cbc.sex,
                cbc__age_min__lt=three_diff.cbc.age,
                cbc__age_max__gt=three_diff.cbc.age,
                diff__value_type=three_diff.value_type
            )
        return context
