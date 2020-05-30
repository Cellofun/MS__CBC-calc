from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from cbc.models import CompleteBloodCount, FiveDiff, BloodSmear
from range.models import ReferenceRange

from cbc.forms import CBCModelForm, FiveDiffFormSet


class FiveDifCreateView(CreateView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_create.html'
    form_class = CBCModelForm

    def get_success_url(self):
        return reverse_lazy('cbc:five-dif-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(FiveDifCreateView, self).get_context_data(**kwargs)
        user = self.request.user
        post = self.request.POST
        if post:
            context['five_dif'] = FiveDiffFormSet(post)
        else:
            context['five_dif'] = FiveDiffFormSet()
        if user.is_authenticated:
            context['cbc'] = CompleteBloodCount.objects.filter(user=user)
            context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        five_dif = context['five_dif']
        cbc = form.instance
        user = self.request.user
        with transaction.atomic():
            cbc.content_type = ContentType.objects.get(app_label='cbc', model='fivediff')
            cbc.object_id = 0
            cbc.type = 5
            if user.is_authenticated:
                cbc.user = user
                cbc.age = user.patient.get_age()
                cbc.sex = user.patient.sex
            self.object = form.save()
            if five_dif.is_valid():
                five_dif.instance = self.object
                five_dif.save()
                fd_object = FiveDiff.objects.get(cbc_id=self.object.id)
                cbc.object_id = fd_object.id
            self.object = form.save()
        return super(FiveDifCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class FiveDifUpdateView(UpdateView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_update.html'
    form_class = CBCModelForm

    def get_success_url(self):
        return reverse_lazy('cbc:five-dif-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(FiveDifUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        post = self.request.POST
        if post:
            context['five_dif'] = FiveDiffFormSet(post, instance=self.object)
        else:
            context['five_dif'] = FiveDiffFormSet(instance=self.object)
        if user.is_authenticated:
            context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        five_dif = context['five_dif']
        with transaction.atomic():
            self.object = form.save()
            if five_dif.is_valid():
                five_dif.instance = self.object
                five_dif.save()
        return super(FiveDifUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class FiveDifDetailView(DetailView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FiveDifDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        five_diff = FiveDiff.objects.get(cbc_id=self.object.id)
        context['five_dif'] = five_diff
        if user.is_authenticated:
            context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=user)
            age = user.patient.get_age()
            context['range'] = ReferenceRange.objects.get(
                cbc__sex=user.patient.sex,
                cbc__age_min__lt=age,
                cbc__age_max__gt=age,
                diff__value_type=five_diff.value_type
            )
        else:
            context['range'] = ReferenceRange.objects.get(
                cbc__sex=five_diff.cbc.sex,
                cbc__age_min__lt=five_diff.cbc.age,
                cbc__age_max__gt=five_diff.cbc.age,
                diff__value_type=five_diff.value_type
            )
        return context
