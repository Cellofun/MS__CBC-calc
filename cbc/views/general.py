from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView

from cbc.models import CompleteBloodCount, BloodSmear, FiveDiff, ThreeDiff
from range.models import CBCRange, IndexRange
from patient.models import Patient


class CBCListView(ListView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_list.html'

    def get_context_data(self, **kwargs):
        context = super(CBCListView, self).get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(user=self.request.user)
        context['blood_smear'] = BloodSmear.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
        return context

    def get_queryset(self):
        return CompleteBloodCount.objects.filter(user=self.request.user)


class CBCDeleteView(DeleteView):
    template_name = 'cbc/cbc_delete.html'
    success_url = reverse_lazy('cbc:cbc-list')

    def get_object(self, **kwargs):
        id_ = self.kwargs.get('id')
        return get_object_or_404(CompleteBloodCount, id=id_)

    def get_context_data(self, **kwargs):
        context = super(CBCDeleteView, self).get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(user=self.request.user)
        context['blood_smear'] = BloodSmear.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
        return context


class CommonChartsTemplateView(TemplateView):
    template_name = 'cbc/cbc_chart_common.html'

    def get_context_data(self, **kwargs):
        context = super(CommonChartsTemplateView, self).get_context_data(**kwargs)
        context['cbc'] = CompleteBloodCount.objects.filter(user=self.request.user)
        context['blood_smear'] = BloodSmear.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
        patient = Patient.objects.get(user=self.request.user)
        age = patient.get_age()
        context['patient'] = patient
        context['range'] = CBCRange.objects.filter(
            sex=patient.sex,
            age_min__lt=age,
            age_max__gt=age
        ).first()
        return context


class IndexChartsTemplateView(TemplateView):
    template_name = 'cbc/cbc_chart_index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexChartsTemplateView, self).get_context_data(**kwargs)
        context['cbc'] = CompleteBloodCount.objects.filter(user=self.request.user)
        context['blood_smear'] = BloodSmear.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
        context['patient'] = Patient.objects.get(user=self.request.user)
        context['range'] = IndexRange.objects.filter().last()
        return context


class DiffChartsTemplateView(TemplateView):
    template_name = 'cbc/cbc_chart_diff.html'

    def get_context_data(self, **kwargs):
        context = super(DiffChartsTemplateView, self).get_context_data(**kwargs)
        context['cbc'] = CompleteBloodCount.objects.filter(user=self.request.user)
        context['three_dif'] = ThreeDiff.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
        context['five_dif'] = FiveDiff.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
        context['blood_smear'] = BloodSmear.objects.filter(cbc__user=self.request.user, cbc__isnull=False)
        context['patient'] = Patient.objects.get(user=self.request.user)
        context['range'] = IndexRange.objects.filter().last()
        return context


class HomeView(TemplateView):
    template_name = 'home/home.html'
